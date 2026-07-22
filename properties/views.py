import json

from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Property, Inquiry, PropertyImage
from .serializers import PropertySerializer, InquirySerializer
from plans.models import Subscription

MAX_PROPERTY_IMAGES = 8


def parse_details(details):
    if not details:
        return {}

    if isinstance(details, dict):
        return details

    if isinstance(details, str):
        try:
            return json.loads(details)
        except json.JSONDecodeError:
            return {}

    return {}


def parse_remove_image_ids(value):
    """
    Frontend sends remove_image_ids as a JSON string:
    "[1, 2, 3]"
    """
    if not value:
        return []

    if isinstance(value, list):
        raw_ids = value
    else:
        try:
            raw_ids = json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return []

    if not isinstance(raw_ids, list):
        return []

    valid_ids = []

    for image_id in raw_ids:
        try:
            valid_ids.append(int(image_id))
        except (TypeError, ValueError):
            continue

    return list(set(valid_ids))


def parse_boolean(value):
    return str(value).strip().lower() in {"true", "1", "yes", "on"}


def delete_gallery_image_file(image_obj):
    """
    Delete both the stored image file and its database record.
    """
    if image_obj.image:
        image_obj.image.delete(save=False)

    image_obj.delete()


class MyPropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "agent":
            return Property.objects.none()

        return Property.objects.filter(
            agent=self.request.user,
        ).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        if request.user.role != "agent":
            return Response(
                {"error": "Only agents can add properties."},
                status=status.HTTP_403_FORBIDDEN,
            )

        subscription = Subscription.objects.filter(
            user=request.user,
            is_active=True,
        ).first()

        if not subscription:
            return Response(
                {"error": "Please choose a plan before adding property."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = timezone.now().date()

        if subscription.end_date < today:
            subscription.is_active = False
            subscription.save(update_fields=["is_active"])

            return Response(
                {"error": "Your plan has expired. Please choose a new plan."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if subscription.remaining_limit() <= 0:
            return Response(
                {
                    "error": (
                        "Your property limit is over. " "Please upgrade your plan."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        main_image = request.FILES.get("main_image")
        gallery_images = request.FILES.getlist("gallery_images")

        total_image_count = (1 if main_image else 0) + len(gallery_images)

        if total_image_count == 0:
            return Response(
                {"main_image": ["Please select at least one property image."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if total_image_count > MAX_PROPERTY_IMAGES:
            return Response(
                {
                    "images": [
                        f"Maximum {MAX_PROPERTY_IMAGES} property images are allowed."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        parsed_details = parse_details(request.data.get("details"))

        data.pop("details", None)
        data.pop("gallery_images", None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            property_obj = serializer.save(
                agent=request.user,
                status="pending",
                expires_at=subscription.end_date,
                edit_locked=False,
                details=parsed_details,
            )

            for image in gallery_images:
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                )

            subscription.property_used += 1
            subscription.save(update_fields=["property_used"])

        return Response(
            self.get_serializer(property_obj).data,
            status=status.HTTP_201_CREATED,
        )


class MyPropertyDetailView(
    generics.RetrieveUpdateDestroyAPIView,
):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "agent":
            return Property.objects.none()

        return Property.objects.filter(agent=self.request.user)

    def update(self, request, *args, **kwargs):
        property_obj = self.get_object()

        if property_obj.edit_locked:
            return Response(
                {
                    "error": (
                        "This property cannot be edited after renewal. "
                        "You can delete it only."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        partial = kwargs.pop("partial", False)

        remove_image_ids = parse_remove_image_ids(
            request.data.get("remove_image_ids"),
        )
        remove_main_image = parse_boolean(
            request.data.get("remove_main_image"),
        )

        new_main_image = request.FILES.get("main_image")
        new_gallery_images = request.FILES.getlist(
            "gallery_images",
        )

        gallery_images_to_remove = list(
            PropertyImage.objects.filter(
                property=property_obj,
                id__in=remove_image_ids,
            )
        )

        remaining_gallery_count = property_obj.images.count() - len(
            gallery_images_to_remove
        )

        current_main_exists = bool(property_obj.main_image)

        final_main_exists = bool(new_main_image) or (
            current_main_exists and not remove_main_image
        )

        if remove_main_image and not new_main_image:
            return Response(
                {"main_image": ["Please select a new main image before updating."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not final_main_exists:
            return Response(
                {"main_image": ["A main property image is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        final_image_count = 1 + remaining_gallery_count + len(new_gallery_images)

        if final_image_count > MAX_PROPERTY_IMAGES:
            return Response(
                {
                    "images": [
                        (
                            f"Maximum {MAX_PROPERTY_IMAGES} total "
                            "property images are allowed."
                        )
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()

        # These fields are handled manually, not by the serializer.
        data.pop("remove_image_ids", None)
        data.pop("remove_main_image", None)
        data.pop("gallery_images", None)

        if "details" in request.data:
            parsed_details = parse_details(
                request.data.get("details"),
            )
            data.pop("details", None)
        else:
            # Preserve the current details when frontend does not send it.
            parsed_details = property_obj.details

        old_main_name = (
            property_obj.main_image.name if property_obj.main_image else None
        )
        old_main_storage = (
            property_obj.main_image.storage if property_obj.main_image else None
        )

        serializer = self.get_serializer(
            property_obj,
            data=data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            property_obj = serializer.save(
                status="pending",
                details=parsed_details,
            )

            for image_obj in gallery_images_to_remove:
                delete_gallery_image_file(image_obj)

            for image in new_gallery_images:
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                )

        new_main_name = (
            property_obj.main_image.name if property_obj.main_image else None
        )

        # A new main image replaced the previous one.
        # Remove the old file from storage after the update succeeds.
        if (
            old_main_name
            and old_main_storage
            and old_main_name != new_main_name
            and old_main_storage.exists(old_main_name)
        ):
            old_main_storage.delete(old_main_name)

        property_obj.refresh_from_db()

        return Response(
            self.get_serializer(property_obj).data,
            status=status.HTTP_200_OK,
        )


class ApprovedPropertyListView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        today = timezone.now().date()

        queryset = Property.objects.filter(
            status="approved",
            expires_at__gte=today,
        ).order_by("-created_at")

        listing_type = self.request.query_params.get(
            "listing_type",
        )
        property_type = self.request.query_params.get(
            "property_type",
        )
        location = self.request.query_params.get("location")

        if listing_type:
            queryset = queryset.filter(
                listing_type=listing_type,
            )

        if property_type:
            queryset = queryset.filter(
                property_type=property_type,
            )

        if location:
            queryset = queryset.filter(
                location__icontains=location,
            )

        return queryset


class ApprovedPropertyDetailView(generics.RetrieveAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        today = timezone.now().date()

        return Property.objects.filter(
            status="approved",
            expires_at__gte=today,
        )


class CreateInquiryView(generics.CreateAPIView):
    serializer_class = InquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        property_id = self.kwargs.get("property_id")
        today = timezone.now().date()

        property_obj = Property.objects.filter(
            id=property_id,
            status="approved",
            expires_at__gte=today,
        ).first()

        if not property_obj:
            return Response(
                {"error": ("Property not found or not available.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(property=property_obj)

            return Response(
                {"message": "Inquiry sent successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class MyInquiriesListView(generics.ListAPIView):
    serializer_class = InquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "agent":
            return Inquiry.objects.none()

        return Inquiry.objects.filter(
            property__agent=self.request.user,
        ).order_by("-created_at")
