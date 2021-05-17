from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [

    path('view/<slug:slug>/', views.profile_detail, name='profile_detail'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('follow/<uuid:profile_id>', views.connect_request, name='connect_request'),
    path('accept/<uuid:event_id>', views.accept_request, name='accept_request'),
    path('reject/<uuid:event_id>', views.reject_request, name='reject_request')

]