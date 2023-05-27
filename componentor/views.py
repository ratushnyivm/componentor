from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    """Generic class-based view for a home page."""

    template_name = "index.html"
