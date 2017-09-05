from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'statnuts/homepage.html'

