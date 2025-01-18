from rest_framework import serializers
from register_e_login.models.post import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'user']
        read_only_fields = ['id', 'created_at']
