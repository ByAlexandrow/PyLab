from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class TestsView(LoginRequiredMixin, TemplateView):
    """."""
    template_name = 'tests/tests.html'
