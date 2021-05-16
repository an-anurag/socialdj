from django.contrib import admin
from .models import Activity, Notifications


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity', 'subtype', 'verb')
    date_hierarchy = 'created'


@admin.register(Notifications)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'unread', 'description')
    date_hierarchy = 'created'
