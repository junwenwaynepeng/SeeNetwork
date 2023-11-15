from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Relation(models.TextChoices):
	friend = "friend", "Friend"
	discussion = "discussion", "Discussion"
	learn = "following", "I learn from "
	teach = "followed", "I taught"

class Status(models.TextChoices):
	pending = "pending", "pending"
	confirm = "confirm", "confirm"

class NotificationVerbs(models.TextChoices):
	friend_request = "friend", "friend request"
	discussion_request = "discussion", "discussion request"
	following_request = "following", "following request"
	followed_request = "followed", "followed request"
	confirm = "confirm", "confirm of your request"
	update = "cvupdate", "information update notification"


class FriendRequest(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
	relationship_type = models.CharField(max_length=20, choices=Relation.choices, default="friend")
	status = models.CharField(max_length=10, choices=Status.choices, default='pending')
	timestamp = models.DateTimeField(auto_now_add=True)

class Relationship(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='relationships')
	friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	relationship_type = models.CharField(max_length=20, choices=Relation.choices)