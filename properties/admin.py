from django.contrib import admin
from .models import Property, Inquiry, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


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
    list_filter = ("status", "property_type", "listing_type")
    search_fields = ("title", "location", "agent__username")
    inlines = [PropertyImageInline]


admin.site.register(Property, PropertyAdmin)
admin.site.register(Inquiry)
admin.site.register(PropertyImage)
