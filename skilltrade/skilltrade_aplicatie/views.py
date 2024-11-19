from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .modele.skills_models import Skill
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Pages
def home(request):
    posts = Post.objects.all()
    return render(request, "home_pages/main.html", {"posts": posts})


def messages(request):
    return render(request, "main_pages/messages.html")


def account(request):
    return render(request, "main_pages/account.html")


def requests(request):
    return render(request, "main_pages/requests.html")


# API


def post_by_id(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "post_page.html", {"post": post})


def posts_by_author(request, author_id):
    posts = Post.objects.filter(author__id=author_id)
    return render(request, "posts_by_author.html", {"posts": posts})


def posts_by_skills_offered(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    posts = Post.objects.filter(skills_offered=skill)
    return render(
        request,
        "posts_by_skills.html",
        {"posts": posts, "skill": skill, "filter_type": "offered"},
    )


def posts_by_skills_needed(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    posts = Post.objects.filter(skills_needed=skill)
    return render(
        request,
        "posts_by_skills.html",
        {"posts": posts, "skill": skill, "filter_type": "needed"},
    )


def post_by_user_and_index(request, author_id, post_id):
    posts = Post.objects.filter(author=author_id).order_by("created_at")
    if post_id <= 0 or post_id > posts.count():
        return render(request, "no_posts.html", {"author": author_id})

    post = posts[post_id - 1]
    return render(request, "post_page.html", {"post": post})


@login_required
def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        skills_offered_ids = request.POST.getlist(
            "skills_offered"
        )  # Handle multiple skills offered
        skill_needed_id = request.POST.get(
            "skills_needed"
        )  # Handle single skill needed

        post = Post.objects.create(title=title, content=content, author=request.user)
        post.skills_offered.set(Skill.objects.filter(id__in=skills_offered_ids))
        if skill_needed_id:
            post.skills_needed.set(Skill.objects.filter(id=skill_needed_id))
        post.save()

        return redirect("/")  # Redirect to the posts list or another page

    skills = Skill.objects.all()  # Get all skills for the form
    return render(request, "add_post.html", {"skills": skills})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        # Check if the logged-in user is the author
        if request.user == post.author:
            post.delete()
            return redirect("/")
        else:
            return HttpResponseForbidden("You are not allowed to delete this post.")

    return redirect("/")
