from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Relation(models.TextChoices):
	friend = "friend", "Friend"
	discussion = "discussion", "Discussion"
	learn = "learn", "I learn from "
	teach = "teach", "I taught"
	other = "other", "Other"

class FriendRequest(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
	relationship_type = models.CharField(max_length=20, choices=Relation.choices, default="friend")
	status = models.CharField(max_length=10, default='pending')
	timestamp = models.DateTimeField(auto_now_add=True)

class Relationship(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='relationships')
	friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	relationship_type = models.CharField(max_length=20, choices=Relation.choices)