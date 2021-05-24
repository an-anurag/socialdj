from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [

    path('view/<slug:slug>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('suggestions/', views.SuggestionView.as_view(), name='suggestions'),
    path('follow/<uuid:profile_id>', views.ConnectRequest.as_view(), name='connect_request'),
    path('accept/<uuid:event_id>/<str:event_type>', views.ProcessRequest.as_view(), name='process_request'),

]