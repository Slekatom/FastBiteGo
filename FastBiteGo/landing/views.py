from django.views.generic import TemplateView, RedirectView


class AboutView(TemplateView):
    template_name = 'landing/landing.html'


