from __future__ import unicode_literals

from django import forms
from django.utils.translation import gettext as _
from django.forms import extras
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, date, timedelta

from userena.forms import SignupForm, AuthenticationForm, EditProfileForm
from captcha.fields import ReCaptchaField
from userena import settings as userena_settings

attrs_dict = {'class': 'required form-control'}
USERNAME_RE = r'^[\.\w]+$'
GENDER_CHOICES = (
    (1, _('Male')),
    (2, _('Female')),)


class SignupFormExtra(SignupForm):

    username = forms.RegexField(regex=USERNAME_RE,

                                max_length=30,

                                widget=forms.TextInput(attrs=attrs_dict),

                                label=_("Username"),

                                error_messages=
                                {'invalid': _('Username must contain only letters, numbers, dots and underscores.')})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Create password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Repeat password"))
    first_name = forms.CharField(label=_(u'First name'), widget=forms.TextInput(attrs=attrs_dict),
                                 max_length=30,
                                 required=True)
    last_name = forms.CharField(label=_(u'Last name'), widget=forms.TextInput(attrs=attrs_dict),
                                max_length=30,
                                required=True)
    gender = forms.ChoiceField(label=_(u'Gender'), widget=forms.Select(attrs=attrs_dict),
                               choices=GENDER_CHOICES,
                               required=True)
    captcha = ReCaptchaField()

    #avatar = forms.ImageField()
    birth_date = forms.DateField(label='Date of birth', widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def clean(self):
        print(self.cleaned_data['birth_date'])
        # print(self.datefield.get)
        print(date.today())
        if (self.cleaned_data['birth_date'] >
                    date.today() - timedelta(18 * 365)):
            raise ValidationError("Musisz miec przynajmniej 18 lat")

        new_user = super(SignupFormExtra, self).save()

        profile = new_user.my_profile
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        profile.birth_date = self.cleaned_data['birth_date']
        profile.gender = self.cleaned_data['gender']
        profile.save()
        new_user.save()

        return new_user


class AuthenticationFormExtra(AuthenticationForm):

    def identification_field_factory(label, error_required):

        return forms.CharField(label=label,
                               widget=forms.TextInput(attrs=attrs_dict),
                               max_length=75,
                               error_messages={'required': error_required})

    identification = identification_field_factory(_("Email or username"), _("Either supply us with your email or username."))

    password = forms.CharField(label=_("Password"),

                               widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))

    remember_me = forms.BooleanField(widget=forms.CheckboxInput(),

                                     required=False,

                                     label=_('Remember me for %(days)s')
                                           % {'days': _(userena_settings.USERENA_REMEMBER_ME_DAYS[0])})


class EditProfileFormExtra(EditProfileForm):
    class Meta(EditProfileForm.Meta):
        exclude = EditProfileForm.Meta.exclude + ['privacy','ban','reputation_points','unban_date','friends','invites','observing_events']
