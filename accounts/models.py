from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models

class Gender(models.TextChoices):
    male = 'm', 'Male'
    female = 'f', 'Female'
    none = 'n', 'Neutral'

class Department(models.TextChoices):
    law = 'law', '法律系'
    me = 'me', '機械系'
    bme = 'bme', '生物機電系'
    chem = 'chem', '化學系'
    ce = 'ce', '化工系'

class CustomUser(AbstractUser):
    # Additional fields for the user profile
    student_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    nick_name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=1, default='n', choices=Gender.choices)
    department = models.CharField(max_length=10, blank=True, null=True, choices=Department.choices)
    display_name = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_student_id = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_nick_name = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_gender = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_department = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])

    def __str__(self):
        return self.username  # You can customize how user objects are displayed.

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'