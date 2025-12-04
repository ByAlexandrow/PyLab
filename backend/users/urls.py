from django.urls import path

from users import views


app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout')
]
