from django.shortcuts import render
from django.http import Http404

from chapters.models import Chapter, Topic


def chapters(request):
    """Showing of all chapters with their topics."""
    chapters = Chapter.objects.filter(is_published=True).prefetch_related('topics').order_by('order')
    return render(request, 'chapters/chapters.html', {'chapters': chapters})


def topic(request, id):
    """Showing one particular topic."""
    try:
        topic = Topic.objects.select_related('chapter').get(
            pk=id, 
            is_published=True,
            chapter__is_published=True
        )
    except Topic.DoesNotExist:
        raise Http404("There is no topic(")
    
    return render(request, 'chapters/topic.html', {'topic': topic})
