from django.db import models

# Create your models here.


from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    property_limit = models.IntegerField()

    def __str__(self):
        return self.name


from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    property_used = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now().date() + timedelta(
                days=self.plan.duration_days
            )
        super().save(*args, **kwargs)

    def remaining_limit(self):
        return self.plan.property_limit - self.property_used

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
