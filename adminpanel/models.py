from django.db import models

# Create your models here.


from django.conf import settings
from django.db import models


class AdminProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_profile",
    )

    admin_title = models.CharField(
        max_length=100,
        default="Master Administrator",
    )

    is_master_admin = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.admin_title}"