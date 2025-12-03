from django.shortcuts import render


def tasks(request):
    """Showing of all chapters with their topics."""
    return render(request, 'tasks/tasks.html',)
