"""
URL configuration for x_app_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from register_e_login.views.inicio_view import inicio_view
from register_e_login.views.home_view import (
    HomeAPIView,
    EditPostAPIView,
    DeletePostAPIView,
    LikePostAPIView,
    CommentPostAPIView
)
from register_e_login.views.login_view import login_view
from register_e_login.views.register_view import register_view
from register_e_login.views.update_user_name_view import UpdateUsernameAPIView, perfil_view, UpdatePasswordAPIView, UpdateProfileAPIView
from register_e_login.views.follow_user import FollowUserAPIView, UnfollowUserAPIView, PostsFromFollowingAPIView
from register_e_login.views.profile_view import ProfileAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio_view, name="inicio"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    
    path('perfil/', perfil_view, name='perfil'),
    path('perfil/atualizar_nome/', UpdateUsernameAPIView.as_view(), name='update_username'),
    path('perfil/atualizar_senha/', UpdatePasswordAPIView.as_view(), name='update_password'),
    path('perfil/atualizar_imagens/', UpdateProfileAPIView.as_view(), name='update_profile_images'),
    
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("profile/<str:username>/", ProfileAPIView.as_view(), name="profile"),

    path("home/", HomeAPIView.as_view(), name="home"),    
    path('api/follow/<int:user_id>/', FollowUserAPIView.as_view(), name='follow_user'),
    path('api/unfollow/<str:username>/', UnfollowUserAPIView.as_view(), name='unfollow_user'),
    path('api/posts/following/', PostsFromFollowingAPIView.as_view(), name='posts_from_following'),

    path('comment/<int:post_id>/', CommentPostAPIView.as_view(), name='comment_post'),  # Adicionando a URL para adicionar comentário
    path('like/<int:post_id>/', LikePostAPIView.as_view(), name='like_post'),
    path("post/<int:post_id>/edit/", EditPostAPIView.as_view(), name="edit_post"),
    path("post/<int:post_id>/delete/", DeletePostAPIView.as_view(), name="delete_post"),

    path("__debug__/", include("debug_toolbar.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


