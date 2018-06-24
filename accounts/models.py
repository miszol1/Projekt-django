from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.db import models
from events.models import Event
import datetime


class MyProfile(UserenaBaseProfile):

    GENDER_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),)


    BAN_CHOICES = (
        (1, _('False')),
        (2, _('True')),)

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')

    birth_date = models.DateField(_('birth date'),
                                  blank=True,
                                  null=True)
    gender = models.PositiveSmallIntegerField(_('gender'),
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)
    about_me = models.TextField(_('about me'),
                                blank=True)

    ban = models.PositiveSmallIntegerField(_('ban'),
                                           choices=BAN_CHOICES,
                                           blank=True,
                                           null=True)
    unban_date = models.DateField(_('unban date'), blank=True, null=True)

    friends = models.ManyToManyField(User, blank=True)

    observing_events = models.ManyToManyField(Event, blank=True, null=True)

    invites = models.ManyToManyField(User, related_name="invites",blank=True)


    # Pole zliczajace punkty reputacji. Eliminujemy w ten sposob koniecznosc kosztownego, kazdorazowego zliczania z tabeli Reputation
    reputation_points = models.IntegerField(blank=True, null=True)



    @property
    def age(self):

        if not self.birth_date:
            return False

        else:

            today = datetime.date.today()

            # Raised when birth date is February 29 and the current year is not a

            # leap year.

            try:

                birthday = self.birth_date.replace(year=today.year)

            except ValueError:

                day = today.day - 1 if today.day != 1 else today.day + 2

                birthday = self.birth_date.replace(year=today.year, day=day)

            if birthday > today:
                return today.year - self.birth_date.year - 1

            else:
                return today.year - self.birth_date.year
