from django.shortcuts import render


def login(request):
    """Showing of all chapters with their topics."""
    return render(request, 'users/login.html',)

def account(request):
    """Showing of all chapters with their topics."""
    return render(request, 'users/account.html',)