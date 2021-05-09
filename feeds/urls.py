from django.urls import path
from . import views

app_name = 'feeds'

urlpatterns = [

    path('', views.get_feeds, name='feeds')
]