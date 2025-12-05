from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class HomepageView(TemplateView):
    """."""
    template_name = 'homepage/index.html'

    @method_decorator(cache_page(60 * 60))
    def dispatch(self, request, *args, **kwargs):
        """."""
        return super().dispatch(request, *args, **kwargs)
