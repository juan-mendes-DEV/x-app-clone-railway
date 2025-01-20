from rest_framework import serializers
from register_e_login.models.like import Like

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]