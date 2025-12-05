from django.shortcuts import render


def index(request):
    """Showing of all chapters with their topics."""
    return render(request, 'homepage/index.html')
