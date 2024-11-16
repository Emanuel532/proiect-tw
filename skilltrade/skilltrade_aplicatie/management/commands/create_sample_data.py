from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from skilltrade_aplicatie.models import Post, Skill

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        python_skill, _ = Skill.objects.get_or_create(name="Python")
        django_skill, _ = Skill.objects.get_or_create(name="Django")
        react_skill, _ = Skill.objects.get_or_create(name="React")
        ml_skill, _ = Skill.objects.get_or_create(name="Machine Learning")
        js_skill, _ = Skill.objects.get_or_create(name="JavaScript")

        user1, _ = User.objects.get_or_create(username="john_doe")
        user2, _ = User.objects.get_or_create(username="jane_smith")
        user3, _ = User.objects.get_or_create(username="alice")

        Post.objects.create(
            title="Looking for Django Expertise",
            content="I need help with a Django project.",
            author=user1,
            skills_offered=python_skill,
            skills_needed=django_skill,
        )
        Post.objects.create(
            title="Frontend Collaboration",
            content="I am offering React expertise and need help with JavaScript.",
            author=user2,
            skills_offered=react_skill,
            skills_needed=js_skill,
        )
        Post.objects.create(
            title="Machine Learning Partner Wanted",
            content="I am looking for someone experienced in Python for ML projects.",
            author=user3,
            skills_offered=ml_skill,
            skills_needed=python_skill,
        )

        self.stdout.write(self.style.SUCCESS("Sample data created!"))
