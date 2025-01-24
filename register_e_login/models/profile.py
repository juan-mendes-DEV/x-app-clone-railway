from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)

    def followers_count(self):
        return self.user.followers.count()

    def following_count(self):
        return self.user.following.count()