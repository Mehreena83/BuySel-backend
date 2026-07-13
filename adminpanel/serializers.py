from rest_framework import serializers
from django.contrib.auth import get_user_model

from properties.models import Property
from plans.models import Plan, Subscription
from payments.models import Payment


User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "role",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
        ]


class AdminPropertySerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source="agent.username", read_only=True)
    agent_email = serializers.CharField(source="agent.email", read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "agent",
            "agent_name",
            "agent_email",
            "title",
            "property_type",
            "listing_type",
            "price",
            "location",
            "main_image",
            "status",
            "expires_at",
            "created_at",
        ]


class AdminPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "price",
            "duration_days",
            "property_limit",
        ]


class AdminSubscriptionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "username",
            "plan",
            "plan_name",
            "start_date",
            "end_date",
            "property_used",
            "is_active",
        ]


class AdminPaymentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "username",
            "plan",
            "plan_name",
            "amount",
            "status",
            "payment_method",
            "razorpay_order_id",
            "razorpay_payment_id",
            "created_at",
        ]