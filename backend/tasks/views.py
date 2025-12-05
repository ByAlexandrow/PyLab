from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class TasksView(LoginRequiredMixin, TemplateView):
    """."""
    template_name = 'tasks/tasks.html'
