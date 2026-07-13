from django.shortcuts import render

# Create your views here.


from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from properties.models import Property
from plans.models import Plan, Subscription
from payments.models import Payment

from .serializers import (
    AdminUserSerializer,
    AdminPropertySerializer,
    AdminPlanSerializer,
    AdminSubscriptionSerializer,
    AdminPaymentSerializer,
)


User = get_user_model()


class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {
            "total_users": User.objects.filter(role="user").count(),
            "total_agents": User.objects.filter(role="agent").count(),
            "total_properties": Property.objects.count(),
            "pending_properties": Property.objects.filter(status="pending").count(),
            "approved_properties": Property.objects.filter(status="approved").count(),
            "rejected_properties": Property.objects.filter(status="rejected").count(),
            "total_plans": Plan.objects.count(),
            "active_subscriptions": Subscription.objects.filter(is_active=True).count(),
            "total_payments": Payment.objects.count(),
            "success_payments": Payment.objects.filter(status="success").count(),
            "failed_payments": Payment.objects.filter(status="failed").count(),
        }

        return Response(data)


class AdminPropertyListView(generics.ListAPIView):
    serializer_class = AdminPropertySerializer
    permission_classes = [IsAdminUser]

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


class AdminApprovePropertyView(APIView):
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.all().order_by("-date_joined")


class AdminPlanListView(generics.ListAPIView):
    serializer_class = AdminPlanSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Plan.objects.all().order_by("price")


class AdminSubscriptionListView(generics.ListAPIView):
    serializer_class = AdminSubscriptionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Subscription.objects.all().order_by("-start_date")


class AdminPaymentListView(generics.ListAPIView):
    serializer_class = AdminPaymentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Payment.objects.all().order_by("-created_at")