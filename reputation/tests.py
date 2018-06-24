from django.test import TestCase

from .models import Reputation
from userena.models import UserenaSignup
from django.core.management import call_command


def create_userena_user(username, password, email):
    return UserenaSignup.objects.create_user(username=username, password=password, email=email)


class ReputationModelTest(TestCase):
    user1_info = {'username': 'amelia',
                  'password': 'test123',
                  'email': 'amelia@localhost'}

    user2_info = {'username': 'bob',
                  'password': 'test123',
                  'email': 'bob@localhost'}

    user3_info = {'username': 'jack',
                  'password': 'test123',
                  'email': 'jack@localhost'}

    user4_info = {'username': 'sarah',
                  'password': 'test123',
                  'email': 'sarah@localhost'}

    def test_model_fields(self):
        call_command('check_permissions')
        usr1 = create_userena_user(**self.user1_info)
        usr2 = create_userena_user(**self.user3_info)

        rep = Reputation.objects.create(from_user=usr2, to_user=usr1, points=3, description="cool person")
        self.assertEquals(rep.description, "cool person")
        self.assertIs(rep.from_user, usr2)
        self.assertIs(rep.to_user, usr1)
        self.assertEquals(rep.points, 3)
        rep2 = Reputation.objects.create(from_user=usr2, to_user=usr1, points=3, description="ok person")
        self.assertEquals(rep2.description, "ok person")

    def test_multiple_entries(self):
        call_command('check_permissions')
        usr1 = create_userena_user(**self.user1_info)
        usr2 = create_userena_user(**self.user3_info)

        rep = Reputation.objects.create(from_user=usr2, to_user=usr1, points=3, description="cool person")
        Reputation.objects.create(from_user=usr2, to_user=usr1, points=3, description="not cool person")
        Reputation.objects.create(from_user=usr1, to_user=usr2, points=3, description="another desc")
        Reputation.objects.create(from_user=usr2, to_user=usr1, points=3, description="cool person")
        Reputation.objects.create(from_user=usr1, to_user=usr2, points=3, description="another desc2")
        filtered_rep_count = Reputation.objects.filter(description="cool person").count()
        all_rep_count = Reputation.objects.count()
        self.assertEquals(filtered_rep_count, 2)
        self.assertEquals(all_rep_count, 5)
