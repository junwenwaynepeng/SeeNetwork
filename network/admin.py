from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Relationship, FriendRequest

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'timestamp')
    search_fields = ('user__username', 'friend__username')


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('sender__username', 'receiver__username')