from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from chapters.models import Chapter, Topic


class ChapterListView(ListView):
    """Chapter's list."""

    model = Chapter
    template_name = 'chapters/chapters.html'
    context_object_name = 'chapters'

    def get_queryset(self):
        """Queryset with prefetch_related."""

        # Unique cash's key
        cache_key = f'chapters_qs_{self.request.user.is_authenticated}'

        # Try to get from existed cash
        queryset = cache.get(cache_key)

        if queryset is not None:
            return queryset

        # Published chapters only
        queryset = Chapter.objects.filter(is_published=True)

        if self.request.user.is_authenticated:
            # Show all published topics
            topics_qs = Topic.objects.filter(is_published=True)
        else:
            # Show only free topics
            topics_qs = Topic.objects.filter(is_published=True, is_free=True)

        topics_qs = topics_qs.order_by('order')

        # Preload topics
        queryset = queryset.prefetch_related(
            Prefetch(
                'topics',
                queryset=topics_qs,
                to_attr='published_topics'
            )
        ).order_by('order')

        # Save cash for 5 mins
        cache.set(cache_key, queryset, 60 * 5)

        return queryset

    def get_context_data(self, **kwargs):
        """Count topics."""

        context = super().get_context_data(**kwargs)
        chapters = context['chapters']

        total_topics = 0
        total_free_topics = 0

        for chapter in chapters:
            total_topics += len(chapter.published_topics)
            for topic in chapter.published_topics:
                if topic.is_free:
                    total_free_topics += 1

        context.update({
            'total_topics': total_topics,
            'total_free_topics': total_free_topics,
            'user_is_authenticated': self.request.user.is_authenticated,
            'page_title': 'Learning Chapters',
            'meta_description': f'Browse {total_topics} topics across {len(chapters)} chapters',
        })

        return context


class TopicDetailView(DetailView):
    """Topic detail."""

    model = Topic
    template_name = 'chapters/topic.html'
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'

    def get_queryset(self):
        """Filter topics."""

        if self.request.user.is_authenticated:
            cache_key = 'topics_qs_auth'
        else:
            cache_key = 'topics_qs_anon'

        queryset = cache.get(cache_key)

        if queryset is not None:
            return queryset

        queryset = Topic.objects.select_related('chapter')

        # Filter topics
        if self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        else:
            queryset = queryset.filter(is_published=True, is_free=True)

        # Save cash
        cache.set(cache_key, queryset, 60 * 5)

        return queryset

    def get_object(self, queryset=None):
        """Topic with cash."""

        if queryset is None:
            queryset = self.get_queryset()

        topic_slug = self.kwargs.get('topic_slug')

        # Ключ кеша для объекта
        if self.request.user.is_authenticated:
            cache_key = f'topic_obj_auth_{topic_slug}'
        else:
            cache_key = f'topic_obj_anon_{topic_slug}'

        # Пробуем получить из кеша
        topic = cache.get(cache_key)

        if topic is None:
            topic = get_object_or_404(queryset, slug=topic_slug)
            cache.set(cache_key, topic, 60 * 60)

        return topic

    def get_context_data(self, **kwargs):
        """
        Контекст с навигацией.
        """
        context = super().get_context_data(**kwargs)
        topic = self.object

        # Получаем топики текущей главы
        # Фильтруем по доступности текущего пользователя
        if self.request.user.is_authenticated:
            chapter_topics = Topic.objects.filter(
                chapter=topic.chapter,
                is_published=True
            ).order_by('order')
        else:
            chapter_topics = Topic.objects.filter(
                chapter=topic.chapter,
                is_published=True,
                is_free=True
            ).order_by('order')

        chapter_topics_list = list(chapter_topics)

        # Находим текущий индекс
        current_index = None
        for i, chap_topic in enumerate(chapter_topics_list):
            if chap_topic.id == topic.id:
                current_index = i
                break

        # Навигация
        previous_topic = None
        next_topic = None
        if current_index is not None:
            if current_index > 0:
                previous_topic = chapter_topics_list[current_index - 1]
            if current_index < len(chapter_topics_list) - 1:
                next_topic = chapter_topics_list[current_index + 1]

        # Цвет для difficulty
        difficulty_classes = {
            'Easy': 'bg-success',
            'Medium': 'bg-warning',
            'Hard': 'bg-danger',
        }

        context.update({
            'chapter': topic.chapter,
            'previous_topic': previous_topic,
            'next_topic': next_topic,
            'current_index': current_index + 1 if current_index is not None else None,
            'total_chapter_topics': len(chapter_topics_list),
            'user_can_access': self.request.user.is_authenticated or topic.is_free,
            'is_free': topic.is_free,
            'estimated_minutes': topic.estimated_minutes,
            'difficulty': topic.difficulty,
            'difficulty_class': difficulty_classes.get(topic.difficulty, 'bg-secondary'),
            'page_title': topic.title,
        })

        return context
