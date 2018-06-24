import datetime

from django.test import TestCase
from django.core.management import call_command

from userena.models import UserenaSignup
from userena import settings as userena_settings
from userena.utils import get_user_profile
from accounts.forms import SignupFormExtra


class MyProfileTest(TestCase):

    def setUp(self):
        call_command('check_permissions')
        self.user = UserenaSignup.objects.create_user(username="testname", email="test@test.test", password="testpass")
        self.user.save()

    def testGoodAge(self):
        exampledate = datetime.date(1997, 1, 1)
        self.user.my_profile.birth_date = exampledate
        today = datetime.date.today()
        age = self.user.my_profile.age
        difference = today.year - exampledate.year
        self.assertEqual(age, difference)

    def testEmptyBirthDate(self):
        self.assertEqual(self.user.my_profile.age, False)

    def testBirthDayBiggerThanToday(self):
        today = datetime.date.today()
        self.user.my_profile.birth_date = today + datetime.timedelta(750)
        self.assertEqual(self.user.my_profile.age, today.year - self.user.my_profile.birth_date.year - 1)

    def testFullName(self):
        user = self.user
        profile = get_user_profile(user=user)
        user.first_name = 'Jan'
        user.last_name = 'Kowalski'
        full_name = profile.get_full_name_or_username()
        self.assertEqual(full_name, "Jan Kowalski")
        user.first_name = ''
        user.last_name = ''
        user.save()
        self.assertEqual(profile.get_full_name_or_username(), "testname")
        userena_settings.USERENA_WITHOUT_USERNAMES = True
        self.assertEqual(profile.get_full_name_or_username(), "test@test.test")
        userena_settings.USERENA_WITHOUT_USERNAMES = False

    def testAccountCreation(self):
        form_data = {'username': 'testuser',
                     'email': 'test@test.test',
                     'password1': 'testpass',
                     'password2': 'testpass',
                     'birth_date': datetime.date(1997, 1, 1),
                     'first_name': 'testfname',
                     'last_name': 'testlname',
                     'gender': '1'}
        new_form = SignupFormExtra()
        new_form.cleaned_data = form_data
        new_user = new_form.clean()
        self.assertEqual(new_user.username, 'testuser')
        self.assertEqual(new_user.email, 'test@test.test')
        self.assertEqual(new_user.my_profile.birth_date, datetime.date(1997, 1, 1))
        self.assertEqual(new_user.first_name, 'testfname')
        self.assertEqual(new_user.last_name, 'testlname')








