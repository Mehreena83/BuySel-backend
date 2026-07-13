from django.contrib import admin
from .models import Property, Inquiry, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


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
        "expires_at",
        "created_at",
    )

    list_filter = (
        "status",
        "property_type",
        "listing_type",
        "location",
    )

    search_fields = (
        "title",
        "location",
        "agent__username",
    )

    inlines = [PropertyImageInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "agent",
                    "title",
                    "description",
                    "property_type",
                    "listing_type",
                    "price",
                    "location",
                    "address",
                    "main_image",
                )
            },
        ),
        (
            "Common Details",
            {
                "fields": (
                    "bedrooms",
                    "bathrooms",
                    "area_sqft",
                )
            },
        ),
        (
            "House / Villa Details",
            {
                "fields": (
                    "total_rooms",
                    "floors",
                    "parking",
                    "furnishing",
                )
            },
        ),
        (
            "Apartment Details",
            {
                "fields": (
                    "floor_number",
                    "total_floors",
                )
            },
        ),
        (
            "Land Details",
            {
                "fields": (
                    "total_cent",
                    "price_per_cent",
                    "road_access",
                    "plot_type",
                )
            },
        ),
        (
            "Commercial Details",
            {
                "fields": (
                    "commercial_type",
                    "builtup_area_sqft",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "expires_at",
                    "edit_locked",
                )
            },
        ),
        (
            "Old JSON Details",
            {
                "fields": ("details",),
                "classes": ("collapse",),
            },
        ),
    )


admin.site.register(Inquiry)
admin.site.register(PropertyImage)
