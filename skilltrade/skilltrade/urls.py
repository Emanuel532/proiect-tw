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
    path('admin/', admin.site.urls),
    path('posts/', views.post_list, name='posts'),
    path('posts/<int:post_id>/', views.post_by_id, name='post_by_id'),
    path('author/<int:author_id>/posts/', views.posts_by_author, name='posts_by_author_id'),
    path('posts/<int:author_id>/<int:post_id>/', views.post_by_user_and_index, name='post_by_user_and_index'),
    path('skills/<int:skill_id>/offered/', views.posts_by_skills_offered, name='posts_by_skills_offered'),
    path('skills/<int:skill_id>/needed/', views.posts_by_skills_needed, name='posts_by_skills_needed'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),

]
