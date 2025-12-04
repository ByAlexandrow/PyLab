from django.urls import path
from django.contrib.auth import views as auth_views

from users import views


app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='users:login',
    ), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('premium/', views.PremiumView.as_view(), name='premium'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]
