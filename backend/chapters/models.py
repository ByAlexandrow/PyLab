from django.db import models

from chapters.mixins import BaseModelMixin, OrderingMixin


class Chapter(BaseModelMixin, OrderingMixin, models.Model):
    """Chapter's model."""

    class Meta(OrderingMixin.Meta):
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
    
    def __str__(self):
        return f'{self.title} - {self.order} - {self.is_published}'


class Topic(BaseModelMixin, OrderingMixin, models.Model):
    """Topic's model."""

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name='Topics'
    )
    content = models.TextField()

    class Meta(OrderingMixin.Meta):
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
    
    def __str__(self):
        return f'{self.title} - {self.chapter} - {self.order} - {self.is_published}'
