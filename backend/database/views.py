from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DatabaseView(TemplateView):
    """."""
    template_name = 'database/database.html'
