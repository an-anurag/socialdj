from django.shortcuts import render
from django.views import View

from notifications.models import Notifications
# Create your views here.


class NotificationsView(View):

    template_name = 'notifications/notifications.html'

    def get(self, request):
        # show only unread notifications
        # categories the notification according to activity type
        notifications = Notifications.objects.filter(recipient=request.user.profile)
        return render(request, self.template_name, {'notifications': notifications})
