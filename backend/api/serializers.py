from rest_framework import serializers

from chapters.models import Chapter, Topic


class BaseSerializerMixin:
    """Mixin for the common serializers."""

    base_fields = ['id', 'title', 'description', 'order', 'is_published']


class ChapterSerializer(BaseSerializerMixin, serializers.ModelSerializer):
    """Chapter's serializer."""

    topics_count = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = BaseSerializerMixin.base_fields + ['topics_count']
    
    def get_topics_count(self, obj):
        """Amount topics in the chapter."""
        return obj.topics.count()


class TopicSerializer(BaseSerializerMixin, serializers.ModelSerializer):
    """Topic's serializer."""

    chapter_title = serializers.CharField(source='chapter.title', read_only=True)

    class Meta:
        model = Topic
        fields = (
            'chapter', 'chapter_title', 'content'
        )
    
    def validate_order(self, value):
        """Order validation."""
        if value < 0:
            raise serializers.ValidationError("Order can't be negative")
        return value


class ChapterWithTopicsSerializer(ChapterSerializer):
    """Chapters with topic."""
    
    topics = TopicSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chapter
        fields = ChapterSerializer.Meta.fields + ['topics']
