from django.db import models

# Create your models here.


from django.conf import settings
from django.db import models


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        PROPERTY_SUBMITTED = (
            "property_submitted",
            "Property Submitted",
        )
        PROPERTY_APPROVED = (
            "property_approved",
            "Property Approved",
        )
        PROPERTY_REJECTED = (
            "property_rejected",
            "Property Rejected",
        )
        PAYMENT = (
            "payment",
            "Payment",
        )
        SUBSCRIPTION = (
            "subscription",
            "Subscription",
        )
        INQUIRY = (
            "inquiry",
            "Inquiry",
        )
        GENERAL = (
            "general",
            "General",
        )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        default=NotificationType.GENERAL,
    )

    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_notifications",
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.recipient.username} - "
            f"{self.title}"
        )