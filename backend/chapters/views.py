from django.shortcuts import render, get_object_or_404

from chapters.models import Chapter


def chapter(request, id):
    chapter = get_object_or_404(
        Chapter.objects.prefetch_related('topics'), pk=id, is_published=True
    )
    return render(request, 'chapters/chapter.html', {'chapter': chapter})
