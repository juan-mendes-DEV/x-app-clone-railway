from rest_framework import serializers
from register_e_login.models.profile import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_image', 'cover_image']

class UserSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Inclua apenas os campos necessários