from django.urls import path

from tasks import views


app_name = 'tasks'

urlpatterns = [
    path('tasks/', views.tasks, name='tasks'),
]
