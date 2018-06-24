from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import MyProfile
from userena.utils import signin_redirect, get_profile_model, get_user_profile
from django.contrib.auth.decorators import login_required
from czaswolny.decorators import user_not_banned
from django.views.decorators.http import require_POST
from events.models import Event


def home(request):
    if request.user.is_authenticated():
        events = Event.objects.all().filter(users=request.user)
        return render(request, 'home.html', {'activepage': 'home', 'usernm': request.user.email, 'events': events})
    else:
        return render(request, 'guest/home.html', {'activepage': 'home'})


def about(request):
    if request.user.is_authenticated():
        return render(request, 'about.html', {'activepage': 'about', 'usernm': request.user.email})
    else:
        return render(request, 'guest/about.html', {'activepage': 'about'})


@require_POST
@login_required
@user_not_banned
def addfriend(request, pk):
    friend = get_object_or_404(MyProfile, user_id=pk)
    if request.user.my_profile != friend:
        request.user.my_profile.friends.add(friend.user)
        friend.friends.add(request.user)
        request.user.my_profile.invites.remove(friend.user)

    return render(request, 'userena/profile_detail.html', {'profile': request.user.my_profile})


@require_POST
@login_required
@user_not_banned
def invite(request, pk):
    friend = get_object_or_404(MyProfile, user_id=pk)
    if request.user.my_profile != friend:
        friend.invites.add(request.user)

    return render(request, 'userena/profile_detail.html', {'profile': friend})


@require_POST
@login_required
@user_not_banned
def refuseinvite(request, pk):
    friend = get_object_or_404(MyProfile, user_id=pk)
    if request.user.my_profile != friend:
        request.user.my_profile.invites.remove(friend.user)

    return render(request, 'userena/profile_detail.html', {'profile': request.user.my_profile})


@require_POST
@login_required
@user_not_banned
def unfriend(request, pk):
    friend = get_object_or_404(MyProfile, user_id=pk)
    request.user.my_profile.friends.remove(friend.user)
    friend.user.my_profile.friends.remove(request.user)

    return render(request, 'userena/profile_detail.html', {'profile': friend})


@require_POST
@login_required
@user_not_banned
def uninvite(request, pk):
    friend = get_object_or_404(MyProfile, user_id=pk)
    friend.invites.remove(request.user)

    return render(request, 'userena/profile_detail.html', {'profile': friend})
