from rest_framework.views import APIView
from rest_framework.response import Response
from register_e_login.models.post import Post
from register_e_login.serializers.post_serializer import PostSerializer
from register_e_login.models import Comment
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer


class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        # Lista os posts de todos os usuários
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response({"posts": serializer.data}, template_name="home.html")

    def post(self, request):
        # Captura apenas o conteúdo do texto
        content = request.data.get("content", "").strip()  # Usando request.data
        if not content:
            posts = Post.objects.all().order_by("-created_at")
            posts_serializer = PostSerializer(posts, many=True)
            return Response(
                {
                    "posts": posts_serializer.data,
                    "errors": {"content": ["O conteúdo não pode estar vazio."]},
                },
                template_name="home.html",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Cria um novo post
        post = Post.objects.create(user=request.user, content=content)
        post.save()

        # Recarrega os posts e retorna à página inicial
        posts = Post.objects.all().order_by("-created_at")
        posts_serializer = PostSerializer(posts, many=True)
        return Response({"posts": posts_serializer.data}, template_name="home.html")


class EditPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            raise Http404("Você não tem permissão para editar este post.")

        # Serializa o post para exibição
        serializer = PostSerializer(post)
        return Response({"post": serializer.data}, template_name="edit_post.html")

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.user != request.user:
            raise Http404("Você não tem permissão para editar este post.")

        # Atualiza o conteúdo do post
        content = request.POST.get("content", "").strip()
        if not content:
            return Response(
                {
                    "post": post,
                    "errors": {"content": ["O conteúdo não pode estar vazio."]},
                },
                template_name="edit_post.html",
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.content = content
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
            like.delete()  # Remove a curtida se já existe
            return Response({"message": "Like removed."}, status=status.HTTP_200_OK)

        return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)


class CommentPostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        content = request.data.get("content", "").strip()
        if not content:
            return Response(
                {"errors": {"content": ["O comentário não pode estar vazio."]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment = Comment.objects.create(user=request.user, post=post, content=content)
        return Response({"message": "Comment added.", "comment_id": comment.id})