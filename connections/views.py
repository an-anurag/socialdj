from django.shortcuts import render
from django.views import View


class ConnectionsListView(View):

    template_name = 'connections/connections.html'

    def get(self, request):
        connections = []
        cons = self.request.user.profile.follows.all()
        for req in cons:
            if req.status == 'accepted':
                connections.append(req.to_profile)
        return render(self.request, self.template_name, {'connections': connections})
