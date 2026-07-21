from rest_framework import serializers

from .models import Notification


class NotificationSerializer(
    serializers.ModelSerializer
):
    property_id = serializers.IntegerField(
        source="property.id",
        read_only=True,
        allow_null=True,
    )

    property_title = serializers.CharField(
        source="property.title",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Notification

        fields = [
            "id",
            "title",
            "message",
            "notification_type",
            "property_id",
            "property_title",
            "is_read",
            "created_at",
        ]

        read_only_fields = fields