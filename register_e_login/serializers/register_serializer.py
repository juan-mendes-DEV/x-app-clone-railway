from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("As senhas não coincidem.")
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # Remover o campo antes de salvar
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
