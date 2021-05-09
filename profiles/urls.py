from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [

    path('<slug:slug>/', views.profile_detail, name='profile_detail'),

]