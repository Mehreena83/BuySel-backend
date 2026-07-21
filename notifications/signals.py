from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from properties.models import Property

from .models import Notification


User = get_user_model()


@receiver(post_save, sender=Property)
def notify_admin_about_new_property(
    sender,
    instance,
    created,
    **kwargs,
):
    # New property create cheyyumbo mathram
    if not created:
        return

    # Agent submitted pending property mathram
    if instance.status != "pending":
        return

    master_admins = User.objects.filter(
        is_active=True,
        is_staff=True,
        is_superuser=True,
        admin_profile__is_master_admin=True,
    )

    agent_name = (
        instance.agent.username
        if instance.agent
        else "Unknown agent"
    )

    notifications = [
        Notification(
            recipient=admin,
            title="New Property Submitted",
            message=(
                f'{agent_name} submitted '
                f'"{instance.title}" for approval.'
            ),
            notification_type=(
                Notification.NotificationType
                .PROPERTY_SUBMITTED
            ),
            property=instance,
        )
        for admin in master_admins
    ]

    if notifications:
        Notification.objects.bulk_create(
            notifications
        )