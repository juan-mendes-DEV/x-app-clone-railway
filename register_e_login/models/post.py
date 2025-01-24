from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    post_likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Adicionando o campo de imagem

    class Meta:
        db_table = "register_e_login_post"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def total_likes(self):
        return self.post_likes.count()