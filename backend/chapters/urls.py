from django.urls import path

from chapters import views


app_name = 'chapters'

urlpatterns = [
    path('chapter/<int:id>/', views.chapter, name='chapter'),
]