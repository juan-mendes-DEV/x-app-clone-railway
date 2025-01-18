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
)
from register_e_login.views.login_view import login_view
from register_e_login.views.register_view import register_view
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
    path("home/", HomeAPIView.as_view(), name="home"),
    path("post/<int:post_id>/edit/", EditPostAPIView.as_view(), name="edit_post"),
    path("post/<int:post_id>/delete/", DeletePostAPIView.as_view(), name="delete_post"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
if settings.DEBUG:  # Apenas para ambiente de desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
