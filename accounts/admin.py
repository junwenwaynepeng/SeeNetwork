from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CurriculumVitae, CustomUser, WorkExperience, EssentialSkill, Award, Publication, Education


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

class CurriculumVitaeAdmin(admin.ModelAdmin):
    list_display = ('user', 'self_introduction',)
    search_fields = ('user', )

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date', 'end_date')
    search_fields = ('position', 'company')

class EssentialSkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name',)
    search_fields = ('skill_name',)

class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'year')
    search_fields = ('title',)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'publication_date')
    search_fields = ('title', 'authors')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('school', 'degree', 'year')
    
admin.site.register(Education, EducationAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(EssentialSkill, EssentialSkillAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CurriculumVitae, CurriculumVitaeAdmin)