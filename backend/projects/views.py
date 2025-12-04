from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProjectsView(LoginRequiredMixin, TemplateView):
    """."""
    template_name = 'projects/projects.html'
