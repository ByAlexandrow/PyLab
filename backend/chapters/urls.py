from django.urls import path

from chapters import views


app_name = 'chapters'

urlpatterns = [
    path('', views.chapters, name='chapters'),
    path('topic/<int:id>/', views.topic, name='topic'),
]
