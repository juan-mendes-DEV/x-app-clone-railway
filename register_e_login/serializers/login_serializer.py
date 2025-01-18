from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Credenciais inválidas.")
        else:
            raise serializers.ValidationError("Ambos os campos são obrigatórios.")
        
        data["user"] = user
        
        # Gerar o token JWT
        refresh = RefreshToken.for_user(user)
        data["access_token"] = str(refresh.access_token)
        data["refresh_token"] = str(refresh)

        return data