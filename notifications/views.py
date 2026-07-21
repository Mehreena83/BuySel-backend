from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from adminpanel.permissions import IsMasterAdmin

from .models import Notification
from .serializers import NotificationSerializer


class AdminNotificationListView(
    generics.ListAPIView
):
    serializer_class = NotificationSerializer
    permission_classes = [IsMasterAdmin]

    def get_queryset(self):
        return (
            Notification.objects
            .filter(recipient=self.request.user)
            .select_related("property")
            .order_by("-created_at")[:50]
        )


class AdminNotificationUnreadCountView(
    APIView
):
    permission_classes = [IsMasterAdmin]

    def get(self, request):
        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).count()

        return Response(
            {
                "unread_count": unread_count,
            },
            status=status.HTTP_200_OK,
        )


class AdminNotificationMarkReadView(
    APIView
):
    permission_classes = [IsMasterAdmin]

    def patch(self, request, pk):
        notification = get_object_or_404(
            Notification,
            id=pk,
            recipient=request.user,
        )

        if not notification.is_read:
            notification.is_read = True

            notification.save(
                update_fields=["is_read"]
            )

        return Response(
            NotificationSerializer(
                notification
            ).data,
            status=status.HTTP_200_OK,
        )


class AdminNotificationMarkAllReadView(
    APIView
):
    permission_classes = [IsMasterAdmin]

    def patch(self, request):
        updated_count = (
            Notification.objects
            .filter(
                recipient=request.user,
                is_read=False,
            )
            .update(is_read=True)
        )

        return Response(
            {
                "message": (
                    "All notifications marked as read."
                ),
                "updated_count": updated_count,
            },
            status=status.HTTP_200_OK,
        )