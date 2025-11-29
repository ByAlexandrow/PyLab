from django.shortcuts import render

from chapters.models import Chapter


def index(request):
    chapters = Chapter.objects.filter(is_published=True)
    return render(request, 'chapters/chapter.html', {'chapters': chapters})
