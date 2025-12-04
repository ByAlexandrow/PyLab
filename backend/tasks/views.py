from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class TasksView(LoginRequiredMixin, TemplateView):
    """."""
    template_name = 'tasks/tasks.html'
