from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skilltrade_aplicatie", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="skills_needed",
        ),
        migrations.RemoveField(
            model_name="post",
            name="skills_offered",
        ),
        migrations.AlterField(
            model_name="skill",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name="post",
            name="skills_needed",
            field=models.ManyToManyField(
                related_name="skills_needed", to="skilltrade_aplicatie.skill"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="skills_offered",
            field=models.ManyToManyField(
                related_name="skills_offered", to="skilltrade_aplicatie.skill"
            ),
        ),
    ]
