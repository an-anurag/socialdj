from django.contrib import admin
from .models import Profile, Connection
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
    list_display = ('id', 'user', 'created')
    list_filter = ('user', 'created')
    date_hierarchy = 'created'


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    search_fields = ('from_profile__user__username',)
    list_display = ('id', 'from_profile', 'to_profile', 'status')
    list_filter = ('from_profile', 'to_profile', 'status')
    date_hierarchy = 'created'
