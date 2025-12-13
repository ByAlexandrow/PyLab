from django.db import models


class Level(models.TextChoices):
    """."""
    BEGINNER = 'beginner', 'Beginner'
    JUNIOR = 'junior', 'Junior'
    MIDDLE = 'middle', 'Middle'
    SENIOR = 'senior', 'Senior'


class Tag(models.Model):
    """."""
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Title'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Published'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'{self.title}'


class Manual(models.Model):
    """Manual's model."""

    title = models.CharField(
        max_length=50,
        null=False,
        verbose_name='Title'
    )
    author = models.CharField(
        max_length=50,
        null=False,
        verbose_name='Author'
    )
    description = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Description'
    )
    manual = models.FileField(
        upload_to='media/manuals/',
        null=False,
        verbose_name='Book'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        default='python-manual',
        verbose_name='Slug'
    )
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER,
        verbose_name='Level'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='manuals',
        blank=True,
        verbose_name='Tag'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Published'
    )

    class Meta():
        verbose_name = 'Manual'
        verbose_name_plural = 'Manuals'

    def __str__(self):
        return f'{self.title} - {self.is_published}'
