from django.contrib import admin
from .models import Post, Skill, ConversationMessage, Request

# Register your models here.

admin.site.register(Post)
admin.site.register(Skill)
admin.site.register(ConversationMessage)
