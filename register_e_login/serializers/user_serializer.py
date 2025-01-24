from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

    def validate_username(self, value):
        """
        Verifica se o nome de usuário já está em uso por outro usuário.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Verifica se a senha antiga está correta
        if not user.check_password(old_password):
            raise serializers.ValidationError("A senha antiga está incorreta.")

        # Verifica se a nova senha e a confirmação são iguais
        if new_password != confirm_password:
            raise serializers.ValidationError("A nova senha e a confirmação não coincidem.")

        # Valida a nova senha com as políticas do Django
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return data