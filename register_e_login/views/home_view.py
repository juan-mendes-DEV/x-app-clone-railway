from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import Http404
from register_e_login.models.post import Post
from register_e_login.models import Comment, Like
from register_e_login.serializers.post_serializer import PostSerializer
from register_e_login.serializers.comment_serializer import CommentSerializer
from register_e_login.serializers.profile_serializer import UserSuggestionSerializer
from django.contrib.auth.models import User
from django.db.models import Q


class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        # Obter os IDs dos usuários que o usuário atual segue
        following_users = request.user.following.values_list('following_id', flat=True)

        # Verificar se o usuário segue alguém
        if following_users:
            # Inclui os posts do próprio usuário (Q(user=request.user)) junto com os posts das pessoas que ele segue
            posts = Post.objects.filter(
                Q(user__id__in=following_users) | Q(user=request.user)
            ).order_by('-created_at')
        else:
            # Se o usuário não segue ninguém, exibe apenas seus próprios posts
            posts = Post.objects.filter(user=request.user).order_by('-created_at')

        user_likes = set(request.user.likes.values_list("post_id", flat=True))
        posts_with_details = []

        for post in posts:
            is_liked_by_user = post.id in user_likes
            post_data = PostSerializer(post).data
            post_data["is_liked_by_user"] = is_liked_by_user
            post_data["likes_count"] = post.likes.count()
            post_data["comments"] = CommentSerializer(post.comments.all(), many=True).data
            posts_with_details.append(post_data)
            print(post_data["comments"])

        # Serializar sugestões de usuários
        suggestions = User.objects.exclude(
            Q(id=request.user.id) | Q(followers__follower=request.user)
        )[:5]
        suggestions_serialized = UserSuggestionSerializer(suggestions, many=True).data

        return Response(
            {"posts": posts_with_details, "suggestions": suggestions_serialized},
            template_name="home.html",  # Retornando o template correto
        )        
    def post(self, request):
        content = request.data.get("content", "").strip()
        image = request.FILES.get("image")  # Obtém a imagem se presente

        if not content and not image:
            return Response(
                {"errors": {"content": ["O conteúdo ou a imagem devem ser fornecidos."]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Criação do post com conteúdo e imagem (se houver)
        Post.objects.create(
            user=request.user,
            content=content,
            image=image  # Salva a imagem se for fornecida
        )
        return redirect("home")

class EditPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [MultiPartParser, FormParser]  # Para permitir upload de arquivos

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            raise Http404("Você não tem permissão para editar este post.")

        serializer = PostSerializer(post)
        return Response({"post": serializer.data}, template_name="edit_post.html")

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            raise Http404("Você não tem permissão para editar este post.")

        content = request.POST.get("content", "").strip()
        image = request.FILES.get("image")  # Obtém a nova imagem, se fornecida

        if not content and not image:
            return Response(
                {"errors": {"content": ["O conteúdo ou a imagem devem ser fornecidos."]}},
                template_name="edit_post.html",
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.content = content
        if image:
            post.image = image  # Atualiza a imagem se for fornecida
        post.save()

        return redirect("home")
        
class DeletePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            raise Http404("Você não tem permissão para deletar este post.")

        post.delete()
        return redirect("home")


class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response(
                {"message": "Like removido.", "likes_count": post.likes.count()},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Post curtido.", "likes_count": post.likes.count()},
            status=status.HTTP_201_CREATED,
        )


class CommentPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        content = request.data.get("content", "").strip()
        if not content:
            return Response(
                {"errors": {"content": ["O comentário não pode estar vazio."]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Comment.objects.create(user=request.user, post=post, content=content)
        return redirect("home")