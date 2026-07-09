from django.urls import path
from .views import (
    MyPropertyListCreateView,
    ApprovedPropertyListView,
    ApprovedPropertyDetailView,
    CreateInquiryView,
    MyInquiriesListView,
    MyPropertyDetailView,
)

urlpatterns = [
    path("my-properties/", MyPropertyListCreateView.as_view(), name="my-properties"),
    path("my-inquiries/", MyInquiriesListView.as_view(), name="my-inquiries"),
    path("approved/", ApprovedPropertyListView.as_view(), name="approved-properties"),
    path(
        "approved/<int:pk>/",
        ApprovedPropertyDetailView.as_view(),
        name="approved-property-detail",
    ),
    path(
        "approved/<int:property_id>/inquiry/",
        CreateInquiryView.as_view(),
        name="create-inquiry",
    ),
    path(
        "my-properties/<int:pk>/",
        MyPropertyDetailView.as_view(),
        name="my-property-detail",
    ),
]
