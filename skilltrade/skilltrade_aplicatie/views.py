from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .modele.skills_models import Skill
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts})

def post_by_id(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_page.html', {'post': post})

def posts_by_author(request, author_id):
    posts = Post.objects.filter(author__id=author_id)
    return render(request, 'posts_by_author.html', {'posts': posts})

def posts_by_skills_offered(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    posts = Post.objects.filter(skills_offered=skill)
    return render(request, 'posts_by_skills.html', {'posts': posts, 'skill': skill, 'filter_type': 'offered'})
def posts_by_skills_needed(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    posts = Post.objects.filter(skills_needed=skill)
    return render(request, 'posts_by_skills.html', {'posts': posts, 'skill': skill, 'filter_type': 'needed'})

def post_by_user_and_index(request, author_id,post_id):
    posts = Post.objects.filter(author=author_id).order_by('created_at')
    if post_id <= 0 or post_id > posts.count():
        return render(request, 'no_posts.html', {'author': author_id})

    post = posts[post_id - 1]
    return render(request, 'post_page.html', {'post': post})

#def landing(request):
 #   return render(request, 'landing.html')   -manu o facut deja landing deci nu mai e nevoie de asta ca root