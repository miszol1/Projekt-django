from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from userena.models import UserenaSignup


class TestViews(TestCase):

    def testHome(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'guest/home.html')

    def testLoggedHome(self):
        call_command('check_permissions')
        user = UserenaSignup.objects.create_user(username="my_name", email="my_name@gmail.com", password="my_password")
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()
        self.client.login(username='my_name', email="my_name@gmail.com", password='my_password')
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def testAbout(self):
        response = self.client.get(reverse('about'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'guest/about.html')

    def testLoggedAbout(self):
        call_command('check_permissions')
        user = UserenaSignup.objects.create_user(username="my_name", email="my_name@gmail.com", password="my_password")
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()
        self.client.login(username='my_name', email="my_name@gmail.com", password='my_password')
        response = self.client.get(reverse('about'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')