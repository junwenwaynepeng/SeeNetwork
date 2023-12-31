from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
from martor.models import MartorField

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
    male = 'm', _('Male')
    female = 'f', _('Female')
    none = 'n', _('Neutral')

class CustomUser(AbstractUser):
    # Additional fields for the user profile
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    nick_name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=1, default='n', choices=Gender.choices)
    slug = models.SlugField(max_length=25, verbose_name=_('User Slug'), unique=True)
    # Social Media Fields
    facebook = models.SlugField(max_length=25, blank=True, null=True)
    x = models.SlugField(max_length=25, blank=True, null=True)
    instagram = models.SlugField(max_length=25, blank=True, null=True)
    linkedin = models.SlugField(max_length=25, blank=True, null=True)
    whatsapp = models.SlugField(max_length=25, blank=True, null=True)
    telegram = models.SlugField(max_length=25, blank=True, null=True)
    discord = models.SlugField(max_length=25, blank=True, null=True)
    tiktok = models.SlugField(max_length=25, blank=True, null=True)
    line = models.SlugField(max_length=25, blank=True, null=True)
    calendly = models.SlugField(max_length=25, blank=True, null=True)
    github = models.SlugField(max_length=25, blank=True, null=True)
    reddit = models.SlugField(max_length=25, blank=True, null=True)
    stackoverflow = models.SlugField(max_length=25, blank=True, null=True)
    youtube = models.SlugField(max_length=25, blank=True, null=True)
    spotify = models.SlugField(max_length=25, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    steam = models.SlugField(max_length=25, blank=True, null=True)
    twitch = models.SlugField(max_length=25, blank=True, null=True)
    orcid = models.SlugField(max_length=25, blank=True, null=True)
    google_scholar = models.SlugField(max_length=25, blank=True, null=True)
    patreon = models.SlugField(max_length=25, blank=True, null=True)
    medium = models.SlugField(max_length=25, blank=True, null=True)
    line = models.SlugField(max_length=25, blank=True, null=True)
    def __str__(self):
        return self.username  # You can customize how user objects are displayed.

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.username))
        super(CustomUser, self).save(*args, **kwargs)
        

class PrivateSetting(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    display_name_on_network = models.BooleanField(default=False)
    display_name = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_student_id = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_nick_name = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_gender = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_department = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    display_cv = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    class Meta:
        verbose_name = _('Private Setting')
        verbose_name_plural = _('Private Settings')

class ProfilePageSetting(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    url = models.URLField(max_length=200, null=True, blank=True, help_text=_('If you set a page link here, we will use this page as your profile page'))
    use_custom_page = models.BooleanField(default=False)

class StudentSetting(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser)
def create_other_setting(sender, instance, created, **kwargs):
    if created:
        private_setting = PrivateSetting.objects.create(user=instance)
        profile_page_setting = ProfilePageSetting.objects.create(user=instance)
        student_setting = StudentSetting.objects.create(user=instance)

class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    school = models.CharField(max_length=50)
    department = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=20)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)])
    def __str__(self):
        if self.department==None:
            return f'{self.school}, {self.degree}, {self.year}'
        else:            
            return f'{self.school}, {self.department}, {self.degree}, {self.year}'


class WorkExperience(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    detail = MartorField(null=True, blank=True)
    def __str__(self):
        return f'{self.position}, {self.company}     {self.start_date}-{self.end_date}\n{self.detail}'


class EssentialSkill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)
    description = MartorField(null=True, blank=True)
    order = models.PositiveSmallIntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)])

    def __str__(self):
        if self.description is not None:
            return self.skill_name
        else:
            return f'{self.skill_name}: {self.description}'

class Award(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, null=True, blank=True)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)])
    high_light = models.BooleanField(default=False)

    def __str__(self):
        if self.organization is not None:
            return f'{self.title} ({self.organization}), {self.year}'
        else:
            return f'{self.title}, {self.year}'

class Publication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    publication_date = models.DateField()
    link = models.URLField(max_length=200, null=True, blank=True)
    high_light = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} ({self.publication_date.year}), {self.authors}'

class SelfDefinedContent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = MartorField(null=True, blank=True)
    form_order = models.PositiveSmallIntegerField()

class SelfIntroduction(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    self_introduction = MartorField(blank=True, null=True)

class CurriculumVitae(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    self_introduction_form_order = models.PositiveSmallIntegerField(default=0)
    education_form_order = models.PositiveSmallIntegerField(default=1)
    work_experience_form_order = models.PositiveSmallIntegerField(default=2)
    essential_skill_form_order = models.PositiveSmallIntegerField(default=3)
    award_form_order = models.PositiveSmallIntegerField(default=4)
    publication_form_order = models.PositiveSmallIntegerField(default=5)
    self_defined_content = models.ManyToManyField(SelfDefinedContent, blank=True)

