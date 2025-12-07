from django.urls import path

from database import views


app_name = 'database'

urlpatterns = [
    path('database/', views.DatabaseView.as_view(), name='database'),
]
