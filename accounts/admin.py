from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CurriculumVitae, CustomUser, WorkExperience, EssentialSkill, Award, Publication, Education, SelfIntroduction, SelfDefinedContent, ProfilePageSetting, PrivateSetting, Contact

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'student_id', 'department', 'is_staff', 'date_joined', 'slug')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id', 'department')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'student_id', 'department', 'slug'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

@admin.register(SelfIntroduction)
class SelfIntroductionAdmin(admin.ModelAdmin):
    list_display = ('user', 'self_introduction')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date', 'end_date')
    search_fields = ('position', 'company')

@admin.register(EssentialSkill)
class EssentialSkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name',)
    search_fields = ('skill_name',)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'year')
    search_fields = ('title',)

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'publication_date')
    search_fields = ('title', 'authors')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school', 'degree', 'year')

@admin.register(SelfDefinedContent)
class SelfDefinedContentAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'form_order')
    search_fields = ('user',)

@admin.register(ProfilePageSetting)
class ProfilePageSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'use_custom_page')
    search_fields = ('user',)

admin.site.register(CustomUser, CustomUserAdmin)