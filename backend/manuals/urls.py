from django.urls import path

from manuals import views


app_name = 'manuals'

urlpatterns = [
    path('manuals/', views.ManualsView.as_view(), name='manuals'),
]
