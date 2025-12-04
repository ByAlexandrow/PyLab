from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, TemplateView):
    """."""
    template_name = 'users/profile.html'


class PremiumView(LoginRequiredMixin, TemplateView):
    """."""
    template_name = 'users/premium.html'


class SettingsView(LoginRequiredMixin, TemplateView):
    """."""
    template_name = 'users/settings.html'
