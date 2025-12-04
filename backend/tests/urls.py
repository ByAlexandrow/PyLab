from django.urls import path

from tests import views


app_name = 'tests'

urlpatterns = [
    path('tests/', views.TestsView.as_view(), name='tests'),
]
