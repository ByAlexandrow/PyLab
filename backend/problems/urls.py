from django.urls import path

from problems import views


app_name = 'problems'

urlpatterns = [
    path('problems/', views.ProblemsView.as_view(), name='problems'),
]
