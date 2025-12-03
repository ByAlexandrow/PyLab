from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, Prefetch

from chapters.models import Chapter, Topic


def chapters(request):
    """Отображение списка глав с топиками."""
    # Фильтруем опубликованные главы
    chapters = Chapter.objects.filter(is_published=True).prefetch_related(
        Prefetch(
            'topics',
            queryset=Topic.objects.filter(is_published=True).order_by('order'),
            to_attr='published_topics'
        )
    ).order_by('order')
    
    # Считаем общую статистику
    total_topics = sum(len(chapter.published_topics) for chapter in chapters)
    
    context = {
        'chapters': chapters,
        'total_topics': total_topics,
    }
    return render(request, 'chapters/chapters.html', context)

def topic(request, id):
    """Детальное отображение топика."""
    topic = get_object_or_404(
        Topic.objects.select_related('chapter'),
        id=id,
        is_published=True
    )
    
    context = {
        'topic': topic,
        'chapter': topic.chapter,
    }
    return render(request, 'chapters/topic.html', context)