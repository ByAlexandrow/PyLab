from django.contrib import admin

from chapters.models import Chapter, Topic


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    fields = (
        'title', 'description',
        'order', 'is_published'
    )
    list_display = ('title', 'order', 'is_published')
    search_fields = ('title', 'order')
    list_filter = ('is_published',)
    ordering = ('order',)
    list_per_page = 20


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    fields = (
        'title', 'description', 'chapter',
        'content', 'order', 'is_published'
    )
    list_display = ('title', 'chapter', 'order', 'is_published')
    search_fields = ('title', 'chapter', 'order')
    list_filter = ('chapter', 'is_published')
    ordering = ('order',)
    list_per_page = 15

