from django.contrib import admin

from chapters.models import Chapter, Topic


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    fields = (
        'title', 'description',
        'order', 'is_published'
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    fields = (
        'title', 'description', 'chapter',
        'content', 'order', 'is_published'
    )

