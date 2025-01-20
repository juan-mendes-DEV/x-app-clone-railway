from rest_framework import serializers
from register_e_login.models.comment import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "user", "content", "created_at"]