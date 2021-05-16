from django.shortcuts import render
from django.contrib.auth.views import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


def page_not_found(request, execption):
    return render(request, '404.html', status=404)