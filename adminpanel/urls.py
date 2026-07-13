from django.urls import path

from .views import (
    AdminDashboardStatsView,
    AdminPropertyListView,
    AdminApprovePropertyView,
    AdminRejectPropertyView,
    AdminUserListView,
    AdminPlanListView,
    AdminSubscriptionListView,
    AdminPaymentListView,
    AdminLoginView,
)


urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("dashboard/", AdminDashboardStatsView.as_view(), name="admin-dashboard"),
    path("properties/", AdminPropertyListView.as_view(), name="admin-properties"),
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
    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("plans/", AdminPlanListView.as_view(), name="admin-plans"),
    path("subscriptions/", AdminSubscriptionListView.as_view(), name="admin-subscriptions"),
    path("payments/", AdminPaymentListView.as_view(), name="admin-payments"),
]