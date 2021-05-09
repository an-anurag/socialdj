from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.


@login_required
def profile_detail(request, slug=None):
    """
    A user profile detail view to land user to their profile page
    """
    profile = Profile.objects.get(slug=slug)
    return render(request, 'profiles/profile.html', context={'profile': profile})

