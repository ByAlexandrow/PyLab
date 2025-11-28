from django.db import models


class Chapter(models.Model):
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
        ordering = ['order']
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
    
    def __str__(self):
        return f'{self.title} - {self.order} - {self.is_published}'


class Topic(models.Model):
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
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name='Topics'
    )
    content = models.TextField()
    order = models.IntegerField(
        default=0,
        verbose_name='Order'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Published'
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
    
    def __str__(self):
        return f'{self.title} - {self.chapter} - {self.order} - {self.is_published}'
