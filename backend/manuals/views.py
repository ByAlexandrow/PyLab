from django.views.generic import ListView, DetailView
from django.db.models import Count, Q

from manuals.models import Manual, Tag


class ManualsListView(ListView):
    """View для отображения списка учебников."""
    model = Manual
    template_name = 'manuals/manuals.html'
    context_object_name = 'manuals'
    
    def get_queryset(self):
        """
        Возвращает только опубликованные учебники.
        """
        queryset = Manual.objects.filter(
            is_published=True
        ).prefetch_related(
            'tag'  # Оптимизация для ManyToMany поля
        ).order_by(
            'title'  # Сортировка по названию
        )
        
        # Фильтрация по тегу из GET-параметра
        tag_slug = self.request.GET.get('tag')
        if tag_slug and tag_slug != 'all':
            queryset = queryset.filter(tag__slug=tag_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Добавляем теги и статистику в контекст."""
        context = super().get_context_data(**kwargs)
        
        # Получаем все опубликованные теги
        # Используем правильный подсчет только опубликованных книг
        tags = Tag.objects.filter(
            is_published=True
        ).annotate(
            manual_count=Count(
                'manuals',
                filter=Q(manuals__is_published=True)
            )
        ).order_by('title')
        
        context['tags'] = tags
        
        # Активный тег для выделения в фильтре
        active_tag_slug = self.request.GET.get('tag')
        context['active_tag'] = active_tag_slug if active_tag_slug else None
        
        # Если хотите получить объект тега для активного фильтра
        if active_tag_slug and active_tag_slug != 'all':
            try:
                context['active_tag_obj'] = Tag.objects.get(slug=active_tag_slug)
            except Tag.DoesNotExist:
                context['active_tag_obj'] = None
        else:
            context['active_tag_obj'] = None
        
        # Получаем все книги для статистики (без фильтрации по тегу)
        all_manuals = Manual.objects.filter(is_published=True)
        
        # Счетчики по уровням для текущего фильтра
        manuals = context['manuals']
        level_counts = {
            'beginner': manuals.filter(level='beginner').count(),
            'junior': manuals.filter(level='junior').count(),
            'middle': manuals.filter(level='middle').count(),
            'senior': manuals.filter(level='senior').count(),
        }
        context['level_counts'] = level_counts
        
        # Общее количество книг для статистики
        context['total_books'] = all_manuals.count()
        
        # Количество тегов с книгами (для статистики)
        tags_with_books = tags.filter(manual_count__gt=0)
        context['tags_count'] = tags_with_books.count()
        
        return context


class ManualDetailView(DetailView):
    """View для детальной страницы учебника."""
    model = Manual
    template_name = 'manuals/manual.html'
    context_object_name = 'manual'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Возвращаем только опубликованные учебники."""
        return Manual.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        """Добавляем связанные учебники в контекст."""
        context = super().get_context_data(**kwargs)
        manual = self.get_object()
        
        # Получаем связанные учебники (по тегам)
        if manual.tag.exists():
            related_manuals = Manual.objects.filter(
                tag__in=manual.tag.all(),
                is_published=True
            ).exclude(
                id=manual.id
            ).distinct().order_by(
                'title'
            )[:3]  # Ограничиваем 3 книгами
            
            context['related_manuals'] = related_manuals
        
        return context