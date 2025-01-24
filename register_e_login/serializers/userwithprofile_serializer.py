from rest_framework import serializers
from django.contrib.auth.models import User
from register_e_login.models.profile import Profile
from register_e_login.serializers.user_serializer import UserSerializer  # Importa o UserSerializer existente

class UserWithProfileSerializer(UserSerializer):
    profile = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['profile']

    def get_profile(self, obj):
        profile = Profile.objects.filter(user=obj).first()
        if profile:
            return {
                "profile_image": profile.profile_image.url if profile.profile_image else None,
                "cover_image": profile.cover_image.url if profile.cover_image else None,
            }
        return None