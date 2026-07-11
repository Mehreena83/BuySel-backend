import json

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone

from .models import Property, Inquiry, PropertyImage
from .serializers import PropertySerializer, InquirySerializer
from plans.models import Subscription


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


class MyPropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "agent":
            return Property.objects.none()

        return Property.objects.filter(agent=self.request.user).order_by("-created_at")

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
            subscription.save()

            return Response(
                {"error": "Your plan has expired. Please choose a new plan."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if subscription.remaining_limit() <= 0:
            return Response(
                {"error": "Your property limit is over. Please upgrade your plan."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()

        parsed_details = parse_details(request.data.get("details"))

        if "details" in data:
            data.pop("details")

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            property_obj = serializer.save(
                agent=request.user,
                status="pending",
                expires_at=subscription.end_date,
                edit_locked=False,
                details=parsed_details,
            )

            gallery_images = request.FILES.getlist("gallery_images")

            for image in gallery_images:
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                )

            subscription.property_used += 1
            subscription.save()

            return Response(
                PropertySerializer(property_obj).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyPropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
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
                    "error": "This property cannot be edited after renewal. You can delete it only."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        parsed_details = parse_details(self.request.data.get("details"))

        property_obj = serializer.save(
            status="pending",
            details=parsed_details,
        )

        gallery_images = self.request.FILES.getlist("gallery_images")

        for image in gallery_images:
            PropertyImage.objects.create(
                property=property_obj,
                image=image,
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

        listing_type = self.request.query_params.get("listing_type")
        property_type = self.request.query_params.get("property_type")
        location = self.request.query_params.get("location")

        if listing_type:
            queryset = queryset.filter(listing_type=listing_type)

        if property_type:
            queryset = queryset.filter(property_type=property_type)

        if location:
            queryset = queryset.filter(location__icontains=location)

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
                {"error": "Property not found or not available."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(property=property_obj)

            return Response(
                {"message": "Inquiry sent successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyInquiriesListView(generics.ListAPIView):
    serializer_class = InquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "agent":
            return Inquiry.objects.none()

        return Inquiry.objects.filter(property__agent=self.request.user).order_by(
            "-created_at"
        )
