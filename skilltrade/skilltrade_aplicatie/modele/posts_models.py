from django.db import models
from django.contrib.auth.models import User

from .skills_models import *
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    skills_offered=models.ManyToManyField(Skill, related_name='skills_offered')
    skills_needed=models.ManyToManyField(Skill, related_name='skills_needed')
    def __str__(self):
        return self.title