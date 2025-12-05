from django.urls import path

from . import views


app_name = 'chapters'

urlpatterns = [
    path('', views.ChapterListView.as_view(), name='chapters'),
    path('topic/<int:id>/', views.TopicDetailView.as_view(), name='topic'),
]
