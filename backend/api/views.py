from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from chapters.models import Chapter, Topic
from api.serializers import (
    ChapterSerializer, 
    TopicSerializer, 
    ChapterWithTopicsSerializer,
    # TopicDetailSerializer
)


class BaseViewSetMixin:
    """Миксин для общих настроек ViewSet"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Возвращает только опубликованные объекты для не-авторизованных"""
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.filter(is_published=True)
        return queryset


class ChapterViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    """ViewSet для глав"""
    
    queryset = Chapter.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChapterWithTopicsSerializer
        return ChapterSerializer
    
    @action(detail=True, methods=['get'])
    def topics(self, request, pk=None):
        """Получить все темы конкретной главы"""
        chapter = self.get_object()
        topics = chapter.topics.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class TopicViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    """ViewSet для тем"""
    
    queryset = Topic.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TopicDetailSerializer
        return TopicSerializer
    
    def get_queryset(self):
        """Фильтрация по главе если передан chapter_id"""
        queryset = super().get_queryset()
        chapter_id = self.request.query_params.get('chapter_id')
        if chapter_id:
            queryset = queryset.filter(chapter_id=chapter_id)
        return queryset
    
    @action(detail=True, methods=['get'])
    def next(self, request, pk=None):
        """Получить следующую тему"""
        topic = self.get_object()
        next_topic = Topic.objects.filter(
            chapter=topic.chapter,
            order__gt=topic.order,
            is_published=True
        ).first()
        
        if next_topic:
            serializer = TopicSerializer(next_topic)
            return Response(serializer.data)
        return Response({"detail": "No next topic"})
