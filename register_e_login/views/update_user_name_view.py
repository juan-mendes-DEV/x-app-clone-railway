from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from register_e_login.serializers.user_serializer import UserSerializer, PasswordSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from register_e_login.models.profile import Profile
from register_e_login.serializers.profile_serializer import ProfileSerializer
from register_e_login.models.post import Post
from django.shortcuts import get_object_or_404
from PIL import Image



@login_required
def perfil_view(request):
    user = request.user

    posts = Post.objects.filter(user=request.user)
    posts_count = posts.count()  # Quantidade de posts

    return render(request, 'perfil.html', {'user': user, 'posts': posts, 'posts_count': posts_count})
    
class UpdateUsernameAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user  # Pega o usuário autenticado

        # Valida e atualiza o nome de usuário usando o serializer
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # Atualiza o usuário com os dados validados
            # Redireciona para a página inicial (home.html)
            return redirect('home')  # Nome da URL de destino
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        if '_method' in request.POST and request.POST['_method'] == 'PATCH':
            return self.patch(request)
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UpdatePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Pega o usuário autenticado

        # Usa o serializer para validar as senhas
        serializer = PasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Se os dados forem válidos, atualiza a senha
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()

            # Atualiza a sessão para evitar logout
            update_session_auth_hash(request, user)

            return redirect('home')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile, _ = Profile.objects.get_or_create(user=user)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            # Validação opcional para imagens
            profile_image = request.FILES.get('profile_image')
            cover_image = request.FILES.get('cover_image')

            if profile_image:
                try:
                    Image.open(profile_image).verify()
                except Exception:
                    return Response({"error": "Imagem de perfil inválida"}, status=400)

            if cover_image:
                try:
                    Image.open(cover_image).verify()
                except Exception:
                    return Response({"error": "Imagem de capa inválida"}, status=400)

            serializer.save()
            return redirect('home')
        else:
            return Response(serializer.errors, status=400)
