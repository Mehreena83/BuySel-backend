from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/plans/", include("plans.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/properties/", include("properties.urls")),
    path("api/admin-panel/", include("adminpanel.urls")),

]
