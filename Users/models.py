# Users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random

class User(AbstractUser):
    # Your custom fields here

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_otp(self, otp):
        print(f"Your OTP is: {otp}")

    def verify_otp(self, otp):
        return self.otp == otp and (timezone.now() - self.otp_created_at).seconds < 300  

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='user_custom_set',  # Unique related_name for custom User model
        related_query_name='user_custom',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='user_custom_set',  # Unique related_name for custom User model
        related_query_name='user_custom',
    )
