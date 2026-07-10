from rest_framework import serializers
from django.utils import timezone
from .models import Property, Inquiry, PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image"]


class PropertySerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source="agent.username", read_only=True)
    is_expired = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "agent",
            "agent_name",
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
            "main_image",
            "status",
            "expires_at",
            "is_expired",
            "edit_locked",
            "created_at",
            "images",
        ]
        read_only_fields = [
            "agent",
            "agent_name",
            "status",
            "expires_at",
            "is_expired",
            "edit_locked",
            "created_at",
        ]

    def get_is_expired(self, obj):
        if not obj.expires_at:
            return False

        return obj.expires_at < timezone.now().date()


class InquirySerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source="property.title", read_only=True)

    class Meta:
        model = Inquiry
        fields = [
            "id",
            "property",
            "property_title",
            "name",
            "phone",
            "message",
            "created_at",
        ]
        read_only_fields = [
            "property",
            "property_title",
            "created_at",
        ]
