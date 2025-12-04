from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.contrib import messages


def login(request):
    """Showing of all chapters with their topics."""
    return render(request, 'users/login.html',)

def profile(request):
    """Showing of all chapters with their topics."""
    return render(request, 'users/profile.html',)

class CustomLogoutView(LogoutView):
    """."""
    next_page = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have been logged out!')
        return super().dispatch(request, *args, **kwargs)
