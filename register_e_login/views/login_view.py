from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from register_e_login.forms import LoginForm  # Caso queira usar um Formulário Django tradicional
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Efetua o login do usuário
            messages.success(request, 'Login bem-sucedido!')
            return redirect('home')  # Redireciona para a página inicial
        else:
            messages.error(request, 'Credenciais inválidas!')
    
    return render(request, 'login.html')