from django.shortcuts import render

# Create your views here.


def get_feeds(request):
    return render(request, 'feeds/feeds.html', {})