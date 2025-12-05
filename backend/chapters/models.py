from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from chapters.mixins import BaseModelMixin, OrderingMixin

from tinymce.models import HTMLField


class Chapter(BaseModelMixin, OrderingMixin, models.Model):
    """Chapter's model."""

    class Meta(OrderingMixin.Meta):
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return f'{self.title} - {self.order} - {self.is_published}'

    @property
    def total_topics_count(self):
        """."""
        return self.topics.filter(is_published=True).count()


class Topic(BaseModelMixin, OrderingMixin, models.Model):
    """Topic's model."""

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name='Chapter'
    )
    content = HTMLField()
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name='Difficulty Level'
    )
    estimated_minutes = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(180)],
        verbose_name='Estimated Reading Time (minutes)',
        help_text='Estimated time to complete this topic in minutes'
    )
    is_free = models.BooleanField(
        default=True,
        verbose_name='Free Access',
        help_text='Is this topic available for free?'
    )

    class Meta(OrderingMixin.Meta):
        ordering = ('order',)
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def __str__(self):
        return f'{self.title} - {self.chapter} - {self.order} - {self.is_published}'
