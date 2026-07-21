from django.urls import path

from .views import (
    AdminDashboardStatsView,
    AdminPropertyListView,
    AdminApprovePropertyView,
    AdminRejectPropertyView,
    AdminUserListView,
    AdminPlanListCreateView,
    AdminPlanDetailView,
    AdminSubscriptionListView,
    AdminPaymentListView,
    AdminLoginView,
    AdminToggleUserStatusView,
AdminPropertyDetailView,
)

from notifications.views import (
    AdminNotificationListView,
    AdminNotificationUnreadCountView,
    AdminNotificationMarkReadView,
    AdminNotificationMarkAllReadView,
)

urlpatterns = [
    path(
        "login/",
        AdminLoginView.as_view(),
        name="admin-login",
    ),

    path(
        "dashboard/",
        AdminDashboardStatsView.as_view(),
        name="admin-dashboard",
    ),

    path(
        "properties/",
        AdminPropertyListView.as_view(),
        name="admin-properties",
    ),

    path(
        "properties/<int:pk>/approve/",
        AdminApprovePropertyView.as_view(),
        name="admin-approve-property",
    ),

    path(
        "properties/<int:pk>/reject/",
        AdminRejectPropertyView.as_view(),
        name="admin-reject-property",
    ),

    path(
        "users/",
        AdminUserListView.as_view(),
        name="admin-users",
    ),

    path(
        "plans/",
        AdminPlanListCreateView.as_view(),
        name="admin-plans",
    ),

    path(
        "plans/<int:pk>/",
        AdminPlanDetailView.as_view(),
        name="admin-plan-detail",
    ),

    path(
        "subscriptions/",
        AdminSubscriptionListView.as_view(),
        name="admin-subscriptions",
    ),

    path(
        "payments/",
        AdminPaymentListView.as_view(),
        name="admin-payments",
    ),
    path(
    "users/<int:pk>/toggle-status/",
    AdminToggleUserStatusView.as_view(),
    name="admin-toggle-user-status",
),
path(
    "properties/<int:pk>/",
    AdminPropertyDetailView.as_view(),
    name="admin-property-detail",
),

path(
    "notifications/",
    AdminNotificationListView.as_view(),
    name="admin-notifications",
),

path(
    "notifications/unread-count/",
    AdminNotificationUnreadCountView.as_view(),
    name="admin-notification-unread-count",
),

path(
    "notifications/<int:pk>/read/",
    AdminNotificationMarkReadView.as_view(),
    name="admin-notification-mark-read",
),

path(
    "notifications/mark-all-read/",
    AdminNotificationMarkAllReadView.as_view(),
    name="admin-notifications-mark-all-read",
),
]