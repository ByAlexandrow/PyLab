from django.urls import path

from . import views


app_name = 'chapters'

urlpatterns = [
    path('', views.ChapterListView.as_view(), name='chapters'),
    path('topic/<slug:topic_slug>/', views.TopicDetailView.as_view(), name='topic'),
]
