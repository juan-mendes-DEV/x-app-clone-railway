from django.db import models
from django.contrib.auth.models import User
from register_e_login.models.post import Post


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")  # Evita duplicidade de curtidas
        db_table = "register_e_login_like"

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"