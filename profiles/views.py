from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View

from .models import Profile, Connection
from notifications.models import Activity, Notifications


class ProfileDetail(View):
    """
    A user profile detail view to land user to their profile page
    """

    template_name = 'profiles/profile.html'

    @method_decorator(login_required)
    def get(self, request, slug=None):
        profile = get_object_or_404(Profile, slug=slug)
        return render(self.request, self.template_name, context={'profile': profile})


class SuggestionView(View):
    """
     Build a recommendation system based on following criteria
     1. Number of common friends

     remember -
     while showing suggestions exclude the current user
     exclude those profiles which are already friends
     exclude those profiles to which there is already a friend request sent
     friend of friend can be friend
     """

    template_name = 'profiles/suggestions.html'

    def get(self, request):

        recommendations = set()

        # find friends of friend
        already_connected = self.request.user.profile.following.all()
        friends_of_friend = []
        for person in already_connected:
            for friend in person.following.all():
                if friend not in already_connected:
                    friends_of_friend.append(friend)

        # for testing only, there shouldn't be global search
        # every friend suggestion must be based on criteria, such as same school, same city
        # below code segment can be omitted
        global_profiles = Profile.objects.exclude(id__in=already_connected).exclude(user_id=self.request.user.id)
        for profile in global_profiles:
            recommendations.add(profile)

        for profile in friends_of_friend:
            recommendations.add(profile)

        return render(self.request, self.template_name, context={'profiles': recommendations})


class ConnectRequest(View):

    def get(self, request, profile_id):
        """
        Send connection request to other profile
        """

        # notifications are generated twice
        # but that needs to be handled in showing recommendations
        to_profile = Profile.objects.get(id=profile_id)
        conn, status = Connection.objects.get_or_create(from_profile=self.request.user.profile, to_profile=to_profile)

        # for notification
        activity = Activity().get_activity(activity='connection', subtype='request')
        actor = self.request.user
        description = actor.username + ' ' + activity.verb
        Notifications.objects.create(
            actor=actor.profile,
            recipient=to_profile,
            activity_type=activity,
            event_id=conn.id,
            description=description
        )
        messages.success(self.request, message='Connection request sent to {}'.format(to_profile.user.username))
        return HttpResponseRedirect(reverse('profiles:suggestions'))


class ProcessRequest(View):

    def get(self, request, event_id, event_type):

        cons = Connection.objects.get(id=event_id)
        if event_type == 'accept':
            cons.accept()
            activity = Activity().get_activity(activity='connection', subtype='accept')
            description = cons.to_profile.username + ' ' + activity.verb
            message = 'You accepted the connection request'
        else:
            cons.reject()
            activity = Activity().get_activity(activity='connection', subtype='reject')
            description = cons.to_profile.username + ' ' + activity.verb
            message = 'You rejected the connection request'

        # for notification
        Notifications.notify(
            actor=cons.to_profile,
            recipient=cons.from_profile,
            activity_type=activity,
            event_id=cons.id,
            description=description
        )
        messages.success(self.request, message=message)
        return HttpResponseRedirect(reverse('profiles:suggestions'))