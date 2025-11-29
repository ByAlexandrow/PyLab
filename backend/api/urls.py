from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChapterViewSet, TopicViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'chapters', ChapterViewSet)
router_v1.register(r'topics', TopicViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
]
