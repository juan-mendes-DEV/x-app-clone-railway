from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )  # Campos a exibir
    list_filter = ("is_staff", "is_active", "date_joined")  # Filtros no admin
    search_fields = ("username", "email")  # Campos para a busca
    ordering = ("date_joined",)  # Ordenação padrão
    list_per_page = 10  # Limita o número de itens exibidos por página no admin


# Remove o registro padrão e registra o personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
