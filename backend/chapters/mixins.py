from django.db import models


class BaseModelMixin(models.Model):
    """Mixin for common model's fields."""
    title = models.CharField(
        max_length=30,
        null=False,
        verbose_name='Title'
    )
    description = models.CharField(
        max_length=100,
        null=False,
        verbose_name='Description'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Order'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Published'
    )

    class Meta:
        abstract = True


class OrderingMixin:
    """Mixin for the base sorting."""

    class Meta:
        ordering = ['order']
