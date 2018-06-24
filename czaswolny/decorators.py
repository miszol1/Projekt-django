from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import date


def user_not_banned(function):
    # Dekorator do sprawdzania czy uzytkownik nie jest zbanowany
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.my_profile.ban != 2 or request.user.is_superuser:
                return function(request, *args, **kwargs)
        if date.today() >= request.user.my_profile.unban_date:
            request.user.my_profile.ban=1
            request.user.my_profile.unban_date = None
            request.user.my_profile.save()
            return function(request, *args, **kwargs)

        return render(request, 'userena/profile_detail.html', {'profile': request.user.my_profile})

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
