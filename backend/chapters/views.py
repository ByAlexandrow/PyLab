from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from chapters.models import Chapter, Topic


class ChapterListView(ListView):
    """
    Список глав с оптимизированными запросами.
    """
    model = Chapter
    template_name = 'chapters/chapters.html'
    context_object_name = 'chapters'

    def get_queryset(self):
        """
        Оптимизированный queryset с prefetch_related.
        """
        # Создаем уникальный ключ кеша
        cache_key = f'chapters_qs_{self.request.user.is_authenticated}'

        # Пробуем получить из кеша
        queryset = cache.get(cache_key)

        if queryset is not None:
            return queryset

        # Базовый queryset - только опубликованные главы
        queryset = Chapter.objects.filter(is_published=True)

        # Создаем отдельный queryset для топиков в зависимости от пользователя
        if self.request.user.is_authenticated:
            # Для авторизованных: все опубликованные топики
            topics_qs = Topic.objects.filter(is_published=True)
        else:
            # Для анонимных: только бесплатные и опубликованные топики
            topics_qs = Topic.objects.filter(is_published=True, is_free=True)

        # Упорядочиваем топики
        topics_qs = topics_qs.order_by('order')

        # Предзагружаем топики
        queryset = queryset.prefetch_related(
            Prefetch(
                'topics',
                queryset=topics_qs,
                to_attr='published_topics'
            )
        ).order_by('order')

        # Сохраняем в кеш на 5 минут
        cache.set(cache_key, queryset, 60 * 5)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Контекст с подсчетом топиков.
        """
        context = super().get_context_data(**kwargs)
        chapters = context['chapters']

        # Считаем топики
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
    """
    Детальный просмотр топика.
    """
    model = Topic
    template_name = 'chapters/topic.html'
    context_object_name = 'topic'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        """
        Фильтруем топики по доступности.
        """
        # Кешируем queryset
        if self.request.user.is_authenticated:
            cache_key = 'topics_qs_auth'
        else:
            cache_key = 'topics_qs_anon'

        queryset = cache.get(cache_key)

        if queryset is not None:
            return queryset

        # Базовый queryset с select_related
        queryset = Topic.objects.select_related('chapter')

        # Фильтруем
        if self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        else:
            queryset = queryset.filter(is_published=True, is_free=True)

        # Сохраняем в кеш
        cache.set(cache_key, queryset, 60 * 5)

        return queryset

    def get_object(self, queryset=None):
        """
        Получаем топик с кешированием объекта.
        """
        if queryset is None:
            queryset = self.get_queryset()

        topic_id = self.kwargs.get('id')

        # Ключ кеша для объекта
        if self.request.user.is_authenticated:
            cache_key = f'topic_obj_auth_{topic_id}'
        else:
            cache_key = f'topic_obj_anon_{topic_id}'

        # Пробуем получить из кеша
        topic = cache.get(cache_key)

        if topic is None:
            topic = get_object_or_404(queryset, pk=topic_id)
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
