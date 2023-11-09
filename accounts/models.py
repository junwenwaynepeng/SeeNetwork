from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models

class CustomUser(AbstractUser):
    # Additional fields for the user profile
    student_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    class_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.username  # You can customize how user objects are displayed.

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'