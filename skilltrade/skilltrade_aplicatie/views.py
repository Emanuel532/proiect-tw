from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .modele.skills_models import Skill
from .models import Post, Request, ConversationMessage, UserContacts
from .forms import RequestForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.timezone import now
from .consumers import ChatConsumer
import logging


# Requests
@login_required
@login_required
def manage_requests(request):
    received_requests = Request.objects.filter(recipient=request.user, status="pending")

    sent_requests = Request.objects.filter(sender=request.user)

    accepted_requests = Request.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user), status="accepted"
    )

    unique_accepted_requests = []
    pairs_seen = set()

    for req in accepted_requests:
        pair = tuple(sorted([req.sender.id, req.recipient.id]))
        if pair not in pairs_seen:
            pairs_seen.add(pair)
            unique_accepted_requests.append(req)

    return render(
        request,
        "manage_requests.html",
        {
            "received_requests": received_requests,
            "sent_requests": sent_requests,
            "accepted_requests": accepted_requests,
        },
    )


@login_required
def respond_request(request, request_id):
    req = get_object_or_404(Request, id=request_id, recipient=request.user)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            if not UserContacts.objects.filter(
                user=req.sender, contacts=req.recipient
            ).exists():
                UserContacts.objects.create(user=req.sender).contacts.add(req.recipient)
            if not UserContacts.objects.filter(
                user=req.recipient, contacts=req.sender
            ).exists():
                UserContacts.objects.create(user=req.recipient).contacts.add(req.sender)
            req.status = "accepted"
            # messages.success(request, "You have accepted the request.")
        elif action == "decline":
            req.status = "declined"
            # messages.success(request, "You have declined the request.")
        req.save()
    return redirect("manage_requests")


# Post search
def post_list(request):
    query = request.GET.get("search", "")
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()

    return render(request, "home.html", {"posts": posts, "query": query})


def filtered_homepage(request):
    query = request.GET.get("search", "")
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(skills_offered__name__icontains=query)
            | Q(skills_needed__name__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.all()

    return render(request, "home_pages/main.html", {"posts": posts, "query": query})


# Pages
def home(request):
    posts = Post.objects.all()
    return render(request, "home_pages/main.html", {"posts": posts})


@login_required
def account(request):
    return render(
        request,
        "main_pages/account.html",
        {"posts": Post.objects.filter(author=request.user), "user": request.user},
    )


def requests(request):
    return render(request, "main_pages/requests.html")


# REQUESTS:


@login_required
def send_request(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Prevent user from requesting their own post
    if post.author == request.user:
        # messages.error(request, "You cannot request your own post.")  # Use messages.error
        return redirect("post_by_id", post_id=post.id)

    # Check if a pending request already exists
    existing_request = Request.objects.filter(
        sender=request.user, post=post, status="pending"
    ).exists()
    if existing_request:
        # messages.error(request, "You have already sent a request for this post.")  # Use messages.error
        return redirect("post_by_id", post_id=post.id)

    # Save the request
    Request.objects.create(
        sender=request.user, recipient=post.author, post=post, status="pending"
    )

    # Add success message
    # messages.success(request, "Your request has been sent.")  # Use messages.success
    return redirect("post_by_id", post_id=post.id)

@login_required
def cancel_request(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Find the pending request sent by the current user
    request_to_cancel = Request.objects.filter(
        sender=request.user, post=post, status="pending"
    ).first()

    if request_to_cancel:
        request_to_cancel.delete()  # Delete the request

    return redirect("post_by_id", post_id=post.id)


# MESSAGES:


@login_required
def send_message(request, recipient_id):
    logging.debug(f"User sender.username sent a message to recipient.username")
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == "POST":
        content = request.POST.get("message")
        if content:
            ConversationMessage.objects.create(
                sender=request.user, recipient=recipient, sent_text=content
            )
        return redirect("conversation", recipient_id=recipient.id)
    sender = request.user
    ChatConsumer.notify_user(recipient.id, sender)
    logging.debug(f"User {sender.username} sent a message to {recipient.username}")
    return redirect("conversation", recipient_id=recipient.id)


@login_required
def view_conversation(request, recipient_id):
    logging.debug(
        f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUser {request.user.username} viewed a conversation with recipient.username"
    )
    recipient = get_object_or_404(User, id=recipient_id)
    messages = ConversationMessage.objects.filter(
        sender__in=[request.user, recipient],
        recipient__in=[request.user, recipient],
    ).order_by("sent_at")
    return render(
        request, "conversation.html", {"recipient": recipient, "messages": messages}
    )


@login_required
def messages_home(request):
    user_contacts = UserContacts.objects.filter(user=request.user).first()

    # Return contacts if user has any, else return an empty list (clearer than User.objects.none())
    contacts = user_contacts.contacts.all() if user_contacts else []

    return render(request, "messages/messages_home.html", {"contacts": contacts})


@login_required
def conversation(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    # Handle POST for sending a message
    if request.method == "POST":
        content = request.POST.get("message")  # Fetch message content from form
        if content:  # Check if the message is not empty
            ConversationMessage.objects.create(
                sender=request.user, recipient=recipient, sent_text=content
            )
            return redirect("conversation", recipient_id=recipient.id)

    # Retrieve messages between the two users
    messages = ConversationMessage.objects.filter(
        sender__in=[request.user, recipient], recipient__in=[request.user, recipient]
    ).order_by("sent_at")

    return render(
        request,
        "messages/conversation.html",
        {"recipient": recipient, "messages": messages},
    )


def check_new_messages(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    unread_messages = ConversationMessage.objects.filter(recipient=request.user)
    return JsonResponse({"unread_count": unread_messages.count()})


# API


@login_required
def post_by_id(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the current user has already sent a request for this post
    existing_request = Request.objects.filter(
        sender=request.user, post=post, status="pending"
    ).exists()

    return render(request, "secondary_pages/post_page.html", {
        "post": post,
        "existing_request": existing_request,
    })



def posts_by_author(request, author_id):
    posts = Post.objects.filter(author__id=author_id)
    return render(request, "secondary_pages/posts_by_author.html", {"posts": posts})


def posts_by_skills_offered(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    posts = Post.objects.filter(skills_offered=skill)
    return render(
        request,
        "secondary_pages/posts_by_skills.html",
        {"posts": posts, "skill": skill, "filter_type": "offered"},
    )


def posts_by_skills_needed(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    posts = Post.objects.filter(skills_needed=skill)
    return render(
        request,
        "secondary_pages/posts_by_skills.html",
        {"posts": posts, "skill": skill, "filter_type": "needed"},
    )


def post_by_user_and_index(request, author_id, post_id):
    posts = Post.objects.filter(author=author_id).order_by("created_at")
    if post_id <= 0 or post_id > posts.count():
        return render(request, "secondary_pages/no_posts.html", {"author": author_id})

    post = posts[post_id - 1]
    return render(request, "secondary_pages/post_page.html", {"post": post})


@login_required
def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        skills_offered_ids = request.POST.getlist("skills_offered")
        skill_needed_id = request.POST.get("skills_needed")

        post = Post.objects.create(title=title, content=content, author=request.user)
        post.skills_offered.set(Skill.objects.filter(id__in=skills_offered_ids))
        if skill_needed_id:
            post.skills_needed.set(Skill.objects.filter(id=skill_needed_id))
        post.save()

        return redirect("/")

    skills = Skill.objects.all()
    return render(request, "secondary_pages/add_post.html", {"skills": skills})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        if request.user == post.author:
            post.delete()
            return redirect("/")
        else:
            return HttpResponseForbidden("You are not allowed to delete this post.")

    return redirect("/")
