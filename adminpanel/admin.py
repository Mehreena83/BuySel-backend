from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import AdminProfile


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "admin_title",
        "is_master_admin",
        "created_at",
    )

    list_filter = (
        "is_master_admin",
    )

    search_fields = (
        "user__username",
        "user__email",
        "admin_title",
    )