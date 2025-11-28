from django.contrib import admin

from topics.models import Topic, Chapter

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    ...


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    ...
