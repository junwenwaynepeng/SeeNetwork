from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from django.utils.text import slugify
import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug
        unique_slug += random_string_generator(size=4)
    return unique_slug

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
    slug = models.SlugField(max_length=25, verbose_name='User Slug', default=student_id, unique=True)
    def __str__(self):
        return self.username  # You can customize how user objects are displayed.

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.username))
        super(CustomUser, self).save(*args, **kwargs)