from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [

    path('view/<slug:slug>/', views.profile_detail, name='profile_detail'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('follow/<uuid:profile_id>', views.connect_request, name='connect_request')

]