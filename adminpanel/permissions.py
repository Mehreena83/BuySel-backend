from rest_framework.permissions import BasePermission


class IsMasterAdmin(BasePermission):
    message = "Master admin access required."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if not user.is_staff or not user.is_superuser:
            return False

        if not hasattr(user, "admin_profile"):
            return False

        return user.admin_profile.is_master_admin is True