from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile, Connection
from notifications.models import Activity, Notifications


# Create your views here.


@login_required
def profile_detail(request, slug=None):
    """
    A user profile detail view to land user to their profile page
    """
    profile = get_object_or_404(Profile, slug=slug)
    return render(request, 'profiles/profile.html', context={'profile': profile})


def suggestions(request):
    """
    Build a recommendation system based on following criteria
    1. Number of common friends

    remember -
    while showing suggestions exclude the current user
    exclude those profiles which are already friends
    exclude those profiles to which there is already a friend request sent
    """

    context = {}
    recommendations = []
    # excluding current user
    recommendations = Profile.objects.exclude(user__username__iexact=request.user.username)
    print(recommendations)
    # TODO: exclude those profiles which are already friends
    # code here and update the context
    connected_profiles = request.user.profile.follows.all()
    suggestions = recommendations.exclude(id__in=[x.id for x in connected_profiles])
    print(suggestions)

    # TODO: exclude those profiles to which there is already a friend request sent
    # code here and update the context
    my_profile = request.user.profile
    cons = Connection.objects.filter(from_profile=my_profile, status='requested')
    print(cons)

    context['profiles'] = recommendations
    return render(request, 'profiles/suggestions.html', context=context)


def connect_request(request, profile_id):
    """
    Send connection request to other profile
    """

    # notifications are generated twice
    # but that needs to be handled in showing recommendations
    to_profile = Profile.objects.get(id=profile_id)
    conn, status = Connection.objects.get_or_create(from_profile=request.user.profile, to_profile=to_profile)

    # for notification
    activity = Activity.objects.filter(activity__iexact='connection', subtype__iexact='request').first()
    actor = request.user
    description = actor.username + ' ' + activity.verb
    Notifications.objects.create(
        actor=actor.profile,
        recipient=to_profile,
        activity_type=activity,
        event_id=conn.id,
        description=description
    )
    messages.success(request, message='Connection request sent to {}'.format(to_profile.user.username))
    return HttpResponseRedirect(reverse('profiles:suggestions'))


def accept_request(request, event_id):
    cons = Connection.objects.get(id=event_id)
    cons.status = 'accepted'
    cons.save()


def reject_request(request, event_id):
    cons = Connection.objects.get(id=event_id)
    cons.status = 'rejected'
    cons.save()
