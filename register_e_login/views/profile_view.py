from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.models import User
from register_e_login.models.post import Post
from register_e_login.serializers.profile_serializer import UserSuggestionSerializer, ProfileSerializer
from register_e_login.serializers.post_serializer import PostSerializer
# from register_e_login.serializers.profile_serializer import ProfileSerializer  # Assumindo que esse serializer existe
from register_e_login.serializers.userwithprofile_serializer import UserWithProfileSerializer
from register_e_login.serializers.comment_serializer import CommentSerializer

from django.db.models import Q

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, username=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=404)

        # Serializa o usuário com o perfil
        user_serialized = UserWithProfileSerializer(user).data

        # Obter os posts do usuário
        posts = Post.objects.filter(user=user).order_by("-created_at")

        # Obter os likes do usuário autenticado
        user_likes = set(request.user.likes.values_list("post_id", flat=True))

        # Serializar os posts com likes e permissões
        posts_with_details = []
        for post in posts:
            is_liked_by_user = post.id in user_likes  # Verifica se o post foi curtido pelo usuário
            post_data = PostSerializer(post).data
            post_data["is_liked_by_user"] = is_liked_by_user
            post_data["likes_count"] = post.likes.count()
            post_data["comments"] = CommentSerializer(post.comments.all(), many=True).data

            # Adiciona o username do usuário no post
            post_data["is_owner"] = post.user == request.user  # Se é o dono do post
            posts_with_details.append(post_data)

        return Response(
            {"user": user_serialized, "posts": posts_with_details},
            template_name="user_profile.html"
        )
        print(posts_with_details)