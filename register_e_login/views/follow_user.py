from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from register_e_login.models.follow import Follow

class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        if request.user != target_user:
            if request.user.following.filter(following=target_user).exists():
                # Deixar de seguir
                request.user.following.filter(following=target_user).delete()
                return Response({"detail": f"Você deixou de seguir {target_user.username}."}, status=status.HTTP_200_OK)
            else:
                # Seguir
                request.user.following.create(following=target_user)
                return redirect("home")
        return Response({"detail": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        # Usuário a ser deixado de seguir
        target_user = get_object_or_404(User, username=username)

        # Remove a relação de "seguindo"
        follow = Follow.objects.filter(follower=request.user, following=target_user).first()
        if follow:
            follow.delete()
            return Response({"detail": f"Você deixou de seguir {username}."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": f"Você não segue {username}."}, status=status.HTTP_400_BAD_REQUEST)


class PostsFromFollowingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obter os IDs dos usuários que o usuário atual segue
        following_users = request.user.following.values_list('following_id', flat=True)
        
        # Verificar se o usuário segue alguém
        if following_users:
            posts = Post.objects.filter(user__id__in=following_users).order_by('-created_at')
        else:
            posts = Post.objects.none()  # Caso o usuário não siga ninguém, retorna uma lista vazia

        # Serializar os posts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)