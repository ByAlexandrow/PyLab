from django.db import models

class Topic(models.Model):
    ...

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
    
    def __str__(self):
        return f''


class Chapter(models.Model):
    ...

    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
    
    def __str__(self):
        return f''
