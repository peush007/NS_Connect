from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('provider', 'Provider'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

class ProviderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='provider_profile')
    full_name = models.CharField(max_length=255, default='')
    service_category = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, related_name='providers_category')
    address = models.CharField(max_length=255, default='', blank=True, help_text="House No, Street, or Colony")
    village_or_area = models.CharField(max_length=255, default='', blank=True, help_text="Village or Area name")
    post_office = models.CharField(max_length=255, default='', blank=True, help_text="Post Office")
    district = models.CharField(max_length=255, default='', blank=True, help_text="District")
    state = models.CharField(max_length=255, default='', blank=True, help_text="State")
    pincode = models.CharField(max_length=10, default='', blank=True, help_text="Pincode")
    experience = models.CharField(max_length=100, default='0 years', help_text="e.g. 5 years")
    pricing = models.CharField(max_length=100, default='Negotiable', help_text="e.g. $50/hr")
    phone_number = models.CharField(max_length=20, default='', blank=True, help_text="Contact number")
    is_approved = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    services = models.ManyToManyField('services.Service', related_name='providers', blank=True)

    def __str__(self):
        return f"Provider: {self.user.username} - {self.full_name}"
