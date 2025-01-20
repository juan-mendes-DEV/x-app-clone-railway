from django.db import models
from django.contrib.auth.models import User
from register_e_login.models.post import Post

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "register_e_login_comment"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"