# Generated by Django 5.1.3 on 2024-11-17 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skilltrade_aplicatie', '0002_remove_post_skills_needed_remove_post_skills_offered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
