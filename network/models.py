from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Status(models.TextChoices):
	pending = "pending", "pending"
	confirm = "confirm", "confirm"

class NotificationVerbs(models.TextChoices):
	following_request = "following", "following request"
	confirm = "confirm", "confirm of your request"
	update = "cvupdate", "information update notification"

class FriendRequest(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
	status = models.CharField(max_length=10, choices=Status.choices, default='pending')
	timestamp = models.DateTimeField(auto_now_add=True)

class Relationship(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_relationships')
	friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_relationships')
	timestamp = models.DateTimeField(auto_now_add=True)