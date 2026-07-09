from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "agent",
        "property_type",
        "listing_type",
        "price",
        "location",
        "status",
        "created_at",
    )
    list_filter = ("status", "property_type", "listing_type", "created_at")
    search_fields = ("title", "location", "agent__username")
    list_editable = ("status",)
