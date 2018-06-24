from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from czaswolny.decorators import user_not_banned
from .models import Reputation
from .forms import AddReputationForm

@login_required
@user_not_banned
def show_received(request, username):
    """
    Widok reputacji, ktore otrzymal dany uzytkownik od innych
    """

    user_shown = get_object_or_404(get_user_model(), username__iexact=username)
    entries = Reputation.objects.filter(to_user=user_shown).order_by('-time_added')
    return render(request, 'reputation/list_received.html',
                  {'user_shown': user_shown, 'user': request.user, 'entries': entries})


@login_required
@user_not_banned
def show_given(request, username):
    """
    Widok reputacji, ktore dany uzytkownik dal innym
    """

    user_shown = get_object_or_404(get_user_model(), username__iexact=username)
    entries = Reputation.objects.filter(from_user=user_shown).order_by('-time_added')
    return render(request, 'reputation/list_given.html',
                  {'user_shown': user_shown, 'user': request.user, 'entries': entries})


@login_required
@user_not_banned
def add(request, username):
    """
    Widok formularza dodawania reputacji pozytywnej/negatywnej
    """

    user_target = get_object_or_404(get_user_model(), username__iexact=username)

    # Czy uzytkownik probuje sam sobie dodac reputacje?
    if user_target == request.user:
        messages.error(request, 'You can\'t add reputation to yourself.')
        return redirect('reputation_show_received', username=user_target.username)

    # Sprawdzamy czy targetowany uzytkownik dostal juz kiedys reputacje od nas
    if Reputation.objects.filter(to_user=user_target, from_user=request.user).exists():
        messages.error(request, 'You have already given reputation to this user.')
        return redirect('reputation_show_received', username=user_target.username)

    if request.method == 'POST':
        form = AddReputationForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            points = int(form.cleaned_data['points'])
            user_reputation = user_target.my_profile.reputation_points
            if user_reputation is None:
                user_reputation = 0

            user_target.my_profile.reputation_points = user_reputation + points
            r = Reputation(from_user=request.user, to_user=user_target, points=points, description=description)
            r.save(force_insert=True)
            user_target.my_profile.save()
            messages.success(request, 'Reputation has been added successfully.')
            return redirect('reputation_show_received', username=user_target.username)

    # GET: dodajemy pusty formularz
    else:
        form = AddReputationForm()

    return render(request, 'reputation/add.html', {'form': form, 'user_target': user_target})
