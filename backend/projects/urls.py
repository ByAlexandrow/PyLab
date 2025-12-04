from django.urls import path

from projects import views


app_name = 'projects'

urlpatterns = [
    path('projects/', views.ProjectsView.as_view(), name='projects'),
]
