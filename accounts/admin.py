from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WorkExperience, SelfIntroduction, EssentialSkill, Award, Publication


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


class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'company', 'start_date', 'end_date')
    search_fields = ('user__username', 'position', 'company')

class SelfIntroductionAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user__username', )

class EssentialSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill_name')
    search_fields = ('user__username', 'skill_name')

class AwardAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'year')
    search_fields = ('user__username', 'title')

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'authors', 'publication_date')
    search_fields = ('user__username', 'title', 'authors')

admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(SelfIntroduction, SelfIntroductionAdmin)
admin.site.register(EssentialSkill, EssentialSkillAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(CustomUser, CustomUserAdmin)