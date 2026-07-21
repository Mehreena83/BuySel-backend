from django.shortcuts import render

# Create your views here.


from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import generics, status
from .permissions import IsMasterAdmin
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from properties.models import Property
from plans.models import Plan, Subscription
from payments.models import Payment
from rest_framework.authtoken.models import Token
from .serializers import (
    AdminUserSerializer,
    AdminPropertySerializer,
    AdminPlanSerializer,
    AdminSubscriptionSerializer,
    AdminPaymentSerializer,
    AdminLoginSerializer,
)
from datetime import timedelta
from django.utils import timezone


User = get_user_model()

class AdminLoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "admin": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "admin_title": user.admin_profile.admin_title,
                        "is_master_admin": user.admin_profile.is_master_admin,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class AdminDashboardStatsView(APIView):
    permission_classes = [IsMasterAdmin]

    def get(self, request):
        recent_properties = Property.objects.all().order_by("-created_at")[:5]
        recent_payments = Payment.objects.all().order_by("-created_at")[:5]

        data = {
            "total_users": User.objects.filter(role="user").count(),
            "total_agents": User.objects.filter(role="agent").count(),

            "total_properties": Property.objects.count(),
            "pending_properties": Property.objects.filter(
                status="pending"
            ).count(),
            "approved_properties": Property.objects.filter(
                status="approved"
            ).count(),
            "rejected_properties": Property.objects.filter(
                status="rejected"
            ).count(),

            "total_plans": Plan.objects.count(),

            "active_subscriptions": Subscription.objects.filter(
                is_active=True
            ).count(),

            "total_payments": Payment.objects.count(),
            "success_payments": Payment.objects.filter(
                status="success"
            ).count(),
            "failed_payments": Payment.objects.filter(
                status="failed"
            ).count(),

            "recent_properties": AdminPropertySerializer(
                recent_properties,
                many=True,
                context={"request": request},
            ).data,

            "recent_payments": AdminPaymentSerializer(
                recent_payments,
                many=True,
                context={"request": request},
            ).data,
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class AdminPropertyListView(generics.ListCreateAPIView):
    serializer_class = AdminPropertySerializer
    permission_classes = [IsMasterAdmin]

    def get_queryset(self):
        queryset = Property.objects.all().order_by("-created_at")

        status_value = self.request.query_params.get("status")
        property_type = self.request.query_params.get("property_type")
        listing_type = self.request.query_params.get("listing_type")

        if status_value:
            queryset = queryset.filter(status=status_value)

        if property_type:
            queryset = queryset.filter(property_type=property_type)

        if listing_type:
            queryset = queryset.filter(listing_type=listing_type)

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            agent=self.request.user,
            status="approved",
            expires_at=timezone.now() + timedelta(days=30),
        )
class AdminApprovePropertyView(APIView):
    permission_classes = [IsMasterAdmin]

    def patch(self, request, pk):
        property_obj = get_object_or_404(Property, id=pk)
        property_obj.status = "approved"
        property_obj.save()

        return Response(
            {
                "message": "Property approved successfully",
                "property": AdminPropertySerializer(property_obj).data,
            },
            status=status.HTTP_200_OK,
        )


class AdminRejectPropertyView(APIView):
    permission_classes = [IsMasterAdmin]

    def patch(self, request, pk):
        property_obj = get_object_or_404(Property, id=pk)
        property_obj.status = "rejected"
        property_obj.save()

        return Response(
            {
                "message": "Property rejected successfully",
                "property": AdminPropertySerializer(property_obj).data,
            },
            status=status.HTTP_200_OK,
        )


class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsMasterAdmin]

    def get_queryset(self):
        return User.objects.all().order_by("-date_joined")


class AdminSubscriptionListView(generics.ListAPIView):
    serializer_class = AdminSubscriptionSerializer
    permission_classes = [IsMasterAdmin]

    def get_queryset(self):
        return Subscription.objects.all().order_by("-start_date")


class AdminPaymentListView(generics.ListAPIView):
    serializer_class = AdminPaymentSerializer
    permission_classes = [IsMasterAdmin]

    def get_queryset(self):
        return Payment.objects.all().order_by("-created_at")
    
class AdminPlanListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminPlanSerializer
    permission_classes = [IsMasterAdmin]

    def get_queryset(self):
        return Plan.objects.all().order_by("price")

    def post(self, request, *args, **kwargs):
        print("POST REQUEST RECEIVED")
        return super().post(request, *args, **kwargs)
class AdminPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminPlanSerializer
    permission_classes = [IsMasterAdmin]
    queryset = Plan.objects.all()

    def delete(self, request, *args, **kwargs):
        plan = self.get_object()

        if plan.subscription_set.exists():
            return Response(
                {
                    "message": (
                        "This plan cannot be deleted because "
                        "subscriptions are linked to it."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan.delete()

        return Response(
            {"message": "Plan deleted successfully"},
            status=status.HTTP_200_OK,
        )
    
class AdminToggleUserStatusView(APIView):
    permission_classes = [IsMasterAdmin]

    def patch(self, request, pk):
        user = get_object_or_404(User, id=pk)

        # സ്വന്തം account block ചെയ്യാൻ പാടില്ല
        if user == request.user:
            return Response(
                {
                    "message": "You cannot block your own account."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = not user.is_active
        user.save()

        return Response(
            {
                "message": (
                    "User activated successfully."
                    if user.is_active
                    else "User blocked successfully."
                ),
                "user": AdminUserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    

class AdminDeletePropertyView(APIView):
    permission_classes = [IsMasterAdmin]

    def delete(self, request, pk):
        property_obj = get_object_or_404(Property, id=pk)

        property_obj.delete()

        return Response(
            {
                "message": "Property deleted successfully."
            },
            status=status.HTTP_200_OK,
        )