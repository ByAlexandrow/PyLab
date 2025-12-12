from django.contrib import admin

from manuals.models import Manual, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    fields = (
        'title', 'author', 'description',
        'manual', 'level', 'tag', 'is_published'
    )
    list_display = ('title', 'author', 'level', 'is_published')
    search_fields = ('title', 'author', 'level', 'tag')
    list_filter = ('author', 'level', 'tag', 'is_published')
    filter_horizontal = ('tag',)
    list_per_page = 20
