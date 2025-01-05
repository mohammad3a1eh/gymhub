from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
    ]

    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
