# Generated by Django 5.1.5 on 2025-01-22 01:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register_e_login", "0005_alter_like_post_alter_like_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="post_likes",
            field=models.ManyToManyField(
                blank=True, related_name="liked_posts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
