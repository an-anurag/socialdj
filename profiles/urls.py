from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('<slug:slug>/', views.profile_detail, name='profile_detail'),

]