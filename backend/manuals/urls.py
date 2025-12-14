from django.urls import path

from manuals import views


app_name = 'manuals'

urlpatterns = [
    path('manuals/', views.ManualsListView.as_view(), name='manuals'),
    path('manual/<slug:manual_slug>/', views.ManualDetailView.as_view(), name='manual'),
]
