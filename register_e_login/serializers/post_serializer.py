from rest_framework import serializers
from register_e_login.models.post import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    image = serializers.ImageField(required=False)
    

    class Meta:
        model = Post
        fields = ["id", "content", "created_at", "image", "user","user_email"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        # Verifica se o conteúdo está vazio e se a imagem não foi fornecida
        if not attrs.get('content') and not attrs.get('image'):
            raise serializers.ValidationError('Você deve fornecer um conteúdo ou uma imagem para o post.')
        return attrs