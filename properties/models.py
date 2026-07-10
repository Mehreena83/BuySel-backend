from django.conf import settings
from django.db import models


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ("house", "House"),
        ("villa", "Villa"),
        ("apartment", "Apartment"),
        ("land", "Land"),
        ("commercial", "Commercial"),
    )

    LISTING_TYPE_CHOICES = (
        ("sale", "Sale"),
        ("rent", "Rent"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties"
    )

    title = models.CharField(max_length=150)
    description = models.TextField()

    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPE_CHOICES)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=150)
    address = models.TextField(blank=True, null=True)

    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.PositiveIntegerField(blank=True, null=True)

    main_image = models.ImageField(upload_to="properties/", blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    expires_at = models.DateField(blank=True, null=True)
    edit_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="properties/gallery/")

    def __str__(self):
        return self.property.title


class Inquiry(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="inquiries"
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.property.title}"
