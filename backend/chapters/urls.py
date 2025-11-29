from django.urls import path

from chapters import views


app_name = 'chapters'

urlpatterns = [
    path('', views.index, name='index'),
]