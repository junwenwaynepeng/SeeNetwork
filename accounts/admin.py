from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'student_id', 'department', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id', 'department')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
    ('Personal info', {
        'fields': ('first_name', 'last_name', 'email', 'student_id', 'department'),
    }),
    ('Permissions', {
        'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    }),
    ('Important dates', {
        'fields': ('last_login', 'date_joined'),
    }),
)

admin.site.register(CustomUser, CustomUserAdmin)