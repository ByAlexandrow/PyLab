from django.views.generic import ListView, DetailView
from django.db.models import Prefetch, Q
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404

from chapters.models import Chapter, Topic


class ChapterListView(ListView):
    """."""
    model = Chapter
    template_name = 'chapters/chapters.html'
    context_object_name = 'chapters'

    def get_queryset(self):
        """."""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        if self.request.user.is_authenticated:
            topic_filter = Q(is_published=True)
        else:
            topic_filter = Q(is_published=True, is_free=True)
        queryset = queryset.prefetch_related(
            Prefetch(
                'topics',
                queryset=Topic.objects.filter(topic_filter).order_by('order'),
                to_attr='published_topics'
            )
        )
        return queryset.order_by('order')
    
    def get_context_data(self, **kwargs):
        """."""
        context = super().get_context_data(**kwargs)
        chapters = context['chapters']
        total_topics = sum(len(chapter.published_topics) for chapter in chapters)
        total_free_topics = sum(
            len([topic for topic in chapter.published_topics if topic.is_free]) for chapter in chapters
        )
        context.update(
            {
                'total_topics': total_topics,
                'total_free_topics': total_free_topics,
                'user_is_authenticated': self.request.user.is_authenticated,
            }
        )
        return context
    
    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        """."""
        return super().dispatch(*args, **kwargs)


class TopicDetailView(DetailView):
    """."""
    model = Topic
    template_name = 'chapters/topic.html'
    context_object_name = 'topic'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        """."""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            result = queryset.filter(is_published=True)
        else:
            result = queryset.filter(is_published=True, is_free=True)
        return result
    
    def get_context_data(self, **kwargs):
        """."""
        context = super().get_context_data(**kwargs)
        topic = self.object
        context['chapter'] = topic.chapter
        context.update(
            {
                'user_can_access': self.request.user.is_authenticated or topic.is_free,
                'is_free': topic.is_free,
                'estimated_minutes': topic.estimated_minutes,
            }
        )
        return context
