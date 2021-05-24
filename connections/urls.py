from django.urls import path
from . import views

app_name = 'connections'

urlpatterns = [
    path('', views.ConnectionsListView.as_view(), name='connections')
]
