"""
URL configuration for skilltrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from skilltrade_aplicatie import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # API
    path("posts/new/", views.add_post, name="add_post"),
    path("post/delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("posts/post_id=<int:post_id>/", views.post_by_id, name="post_by_id"),
    path("send_request/<int:post_id>/", views.send_request, name="send_request"),
    path(
        "author/user_id=<int:author_id>/posts/",
        views.posts_by_author,
        name="posts_by_author_id",
    ),
    path(
        "author/user_id=<int:author_id>/post_id=<int:post_id>/",
        views.post_by_user_and_index,
        name="post_by_user_and_index",
    ),
    path(
        "skills/skill_id=<int:skill_id>/offered/",
        views.posts_by_skills_offered,
        name="posts_by_skills_offered",
    ),
    path(
        "skills/skill_id=<int:skill_id>/needed/",
        views.posts_by_skills_needed,
        name="posts_by_skills_needed",
    ),
    path('post/<int:post_id>/cancel_request/', views.cancel_request, name='cancel_request'),
    # Login
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    # Pages
    path("", views.filtered_homepage, name="filtered_homepage"),
    path("", views.home, name="home"),
    path("account", views.account, name="account"),
    path("requests/", views.manage_requests, name="manage_requests"),
    path(
        "request/<int:request_id>/respond/",
        views.respond_request,
        name="respond_request",
    ),
    path("messages/", views.messages_home, name="messages_home"),
    path(
        "messages/conversation/<int:recipient_id>/",
        views.conversation,
        name="conversation",
    ),
    path(
        "messages/check-new-messages/",
        views.check_new_messages,
        name="check_new_messages",
    ),
    path("send_message/<int:recipient_id>/", views.send_message, name="send_message"),
    # old: path("requests", views.requests, name="requests"),
]
