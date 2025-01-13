from django.db import models
from django.contrib.auth.models import User

from .skills_models import *


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    skills_offered = models.ManyToManyField(Skill, related_name="skills_offered")
    skills_needed = models.ManyToManyField(Skill, related_name="skills_needed")

    def __str__(self):
        return self.title


class Request(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_requests"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_requests"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField(
        blank=True, null=True
    )  # Optional message from the sender
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("declined", "Declined"),
        ],
        default="pending",
    )

    def __str__(self):
        return (
            f"{self.sender.username} -> {self.recipient.username} ({self.post.title})"
        )


class ConversationMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    sent_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username} ({self.sent_text})"
