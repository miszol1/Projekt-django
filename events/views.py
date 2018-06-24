from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import EventForm
from .models import Event
from django.contrib import messages
from notify.signals import notify
from accounts.models import MyProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from czaswolny.decorators import user_not_banned
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
@user_not_banned
def index(request):
    events_all = Event.objects.all().order_by('-start_date')

    # Paginacja co 5 wydarze
    paginator = Paginator(events_all, 5)
    page = request.GET.get('page', 1)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'events/index.html', {'events': events})


@login_required
@user_not_banned
def observing(request):
    profile = get_object_or_404(MyProfile, user_id=request.user.my_profile.user_id)

    events = profile.observing_events.all()

    return render(request, 'events/observing.html', {'events': events})




@login_required
@user_not_banned
def create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            # ponizsza linijka na potrzeby zapisu tagow
            form.save_m2m()
            return redirect('events:details', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/create.html', {'form': form})



@require_POST
@login_required
@user_not_banned
def destroy(request, pk):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))

    event = get_object_or_404(Event, pk=pk)
    if request.user != event.author:
        return HttpResponseRedirect(reverse('events:index'))
    if event.users.all().exists():
        notify.send(request.user, recipient_list=list(event.users.all()), actor=request.user, verb='deleted event you had joined.', nf_type='event_deleted')
    event.delete()
    return redirect('events:index')


@login_required
@user_not_banned
def details(request, pk):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))
    event = get_object_or_404(Event, pk=pk)

    posts_all = event.posts.all().order_by('-publish_date')
    # Paginacja co 5 postow
    posts_paginator = Paginator(posts_all, 5)
    posts_page = request.GET.get('posts-page', 1)
    try:
        posts = posts_paginator.page(posts_page)
    except PageNotAnInteger:
        posts = posts_paginator.page(1)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)

    return render(request, 'events/details.html', {'event': event, 'posts': posts})


@require_POST
@login_required
@user_not_banned
def join(request, pk):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))

    event = get_object_or_404(Event, pk=pk)

    if request.user in event.blacklist.all():
        return HttpResponseRedirect(reverse('events:index'))

    event.users.add(request.user)
    if request.user != event.author:
        notify.send(request.user, recipient=event.author, actor=request.user, verb='joined your event.', nf_type='event_user_joined')

    if request.user not in event.blacklist.all():
        event.users.add(request.user)
    posts = event.posts.all

    if request.user.pk in Event.objects.values_list('users', flat=True):
        messages.success(request, 'Event joined')

    return render(request, 'events/details.html', {'event': event, 'posts': posts})


@require_POST
@login_required
@user_not_banned
def observe(request, pk):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))

    event = get_object_or_404(Event, pk=pk)

    if request.user in event.blacklist.all():
        return HttpResponseRedirect(reverse('events:index'))
    profile = get_object_or_404(MyProfile, user_id=request.user.my_profile.user_id)
    profile.observing_events.add(event)

    posts = event.posts.all

    if request.user.pk in Event.objects.values_list('users', flat=True):
        messages.success(request, 'Event added to your observed events')

    return render(request, 'events/details.html', {'event': event, 'posts': posts})


@require_POST
@login_required
@user_not_banned
def stop_observing(request, pk):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))
    event = get_object_or_404(Event, pk=pk)
    profile = get_object_or_404(MyProfile, user_id=request.user.my_profile.user_id)
    profile.observing_events.add(event)

    profile.observing_events.remove(event)
    posts = event.posts.all
    messages.success(request, 'Event removed from observed events')
    return render(request, 'events/details.html', {'event': event, 'posts': posts})


@require_POST
@login_required
@user_not_banned
def leave(request, pk):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))
    event = get_object_or_404(Event, pk=pk)
    event.users.remove(request.user)
    posts = event.posts.all
    messages.success(request, 'Wypisano z eventu')
    return render(request, 'events/details.html', {'event': event, 'posts': posts})

@login_required
@user_not_banned
def unblock(request, pk, user_id):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.author:
        return HttpResponseRedirect(reverse('events:index'))
    user = get_object_or_404(MyProfile, user_id = user_id)
    event.blacklist.remove(user.user)
    posts = event.posts.all
    messages.success(request, 'Usunieto z blacklisty')
    return render(request, 'events/details.html', {'event': event, 'posts': posts})

@require_POST
@login_required
@user_not_banned
def block(request, pk, user_id):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.author:
        return HttpResponseRedirect(reverse('events:index'))

    user = get_object_or_404(get_user_model(), id=user_id)
    event.blacklist.add(user)

    posts = event.posts.all
    event.users.remove(user)
    messages.success(request, 'Usunieto uzytkownika z eventu')
    return render(request, 'events/details.html', {'event': event, 'posts': posts})


@require_POST
@login_required
@user_not_banned
def like(request, pk):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))

    event = get_object_or_404(Event, pk=pk)
    event.likes.add(request.user)
    posts = event.posts.all
    return render(request, 'events/details.html', {'event': event, 'posts': posts})


@require_POST
@login_required
@user_not_banned
def unlike(request, pk):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))

    event = get_object_or_404(Event, pk=pk)
    event.likes.remove(request.user)
    posts = event.posts.all
    return render(request, 'events/details.html', {'event': event, 'posts': posts})
