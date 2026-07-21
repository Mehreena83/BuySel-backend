from rest_framework import serializers
from django.contrib.auth import get_user_model

from properties.models import Property , PropertyImage
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

class AdminPropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = [
            "id",
            "image",
        ]



class AdminPropertySerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(
        source="agent.username",
        read_only=True,
    )

    agent_email = serializers.CharField(
        source="agent.email",
        read_only=True,
    )

    images = AdminPropertyImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Property

        fields = [
            "id",
            "agent",
            "agent_name",
            "agent_email",
            "title",
            "description",
            "property_type",
            "listing_type",
            "price",
            "location",
            "address",

            "bedrooms",
            "bathrooms",
            "area_sqft",
            "total_floors",
            "floors",
            "parking",
            "furnishing",
            "floor_number",

            "total_cent",
            "price_per_cent",
            "road_access",
            "plot_type",

            "commercial_type",
            "builtup_area_sqft",

            "main_image",
            "images",

            "status",
            "expires_at",
            "created_at",
        ]

        read_only_fields = [
            "agent",
            "status",
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


from django.contrib.auth import authenticate


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get("username"),
            password=data.get("password"),
        )

        if user is None:
            raise serializers.ValidationError("Invalid admin username or password")

        if not user.is_staff or not user.is_superuser:
            raise serializers.ValidationError("Admin access denied")

        if not hasattr(user, "admin_profile"):
            raise serializers.ValidationError("Master admin profile not found")

        if not user.admin_profile.is_master_admin:
            raise serializers.ValidationError("Master admin access denied")

        data["user"] = user
        return data
