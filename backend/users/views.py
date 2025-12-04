from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from users.forms import CustomAuthenticationForm


@require_http_methods(["GET", "POST"])
def logout(request):
    """
    Функция для выхода пользователя (поддерживает GET и POST)
    """
    if request.user.is_authenticated:
        messages.info(request, "You have been successfully logged out.")
    user_logout(request)
    return redirect('users:login')


@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user_login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next', 'users:profile')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password!")
        else:
            messages.error(request, 'Please, correct the errors below!')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required(login_url='users:login')
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})
