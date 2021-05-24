from django.shortcuts import render
from django.views import View

from notifications.models import Notifications
# Create your views here.


class NotificationsView(View):

    template_name = 'notifications/notifications.html'

    def get(self, request):
        conn_updates = Notifications.objects.filter(
            recipient=request.user.profile,
            unread=True,
            activity_type__activity__contains='connection'
        ).order_by('-created')

        # for future feed app
        updates = None
        return render(request, self.template_name, {'conn_updates': conn_updates, 'updates': updates})
