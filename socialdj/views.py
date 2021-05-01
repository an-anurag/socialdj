from django.contrib.auth.views import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'