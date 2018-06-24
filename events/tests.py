from django.test import TestCase
from userena.models import *
from .models import *
from django.core.management import call_command
from .views import *
from django.test import Client


# Create your tests here.


class EventsTestCase(TestCase):
	def test_all(self):
		call_command('check_permissions')
		my_user = UserenaSignup.objects.create_user(username="my_name", email="my_name@gmail.com",
													password="my_password")
		my_user.save()

		my_user2 = UserenaSignup.objects.create_user(username="my_namee", email="my_name@gmail.com",
													 password="my_password")
		my_user2.save()

		self.assertEquals(my_user.username, "my_name")
		self.assertEquals(my_user.email, "my_name@gmail.com")
		self.assertNotEquals(my_user.password, "my_password")
		event1 = Event.objects.create(name="event1", description="gruba impra w akademiku",
									  start_date="2018-03-21", end_date="2018-03-21",
									  place_text="15-001 Bialystok, Polska", place_location_lat=53.0956012,
									  place_location_lng=23.1172786, author=my_user)
		event1.save()

		self.assertEqual(event1.name, "event1")
		self.assertEqual(event1.description, "gruba impra w akademiku")
		self.assertEqual(event1.start_date, "2018-03-21")
		self.assertEqual(event1.end_date, "2018-03-21")
		self.assertEqual(event1.place_text, "15-001 Bialystok, Polska")
		self.assertEqual(event1.place_location_lat, 53.0956012)
		self.assertEqual(event1.place_location_lng, 23.1172786)
		self.assertEqual(event1.author.username, "my_name")
		self.assertIs(event1.author, my_user)
		event2 = Event.objects.create(name="event1", description="gruba impra w akademiku",
									  start_date="2018-03-21", end_date="2018-03-21",
									  place_text="15-001 Bialystok, Polska", place_location_lat=53.0956012,
									  place_location_lng=23.1172786, author=my_user, tags="Domowka")
		event2.save()

		self.assertEqual(event2.tags, "Domowka")
		event2.likes.add(my_user2)
		self.assertIn(my_user2, event2.likes.all())
		self.assertNotIn(my_user, event2.likes.all())
		event2.likes.remove(my_user2)
		self.assertNotIn(my_user2, event2.likes.all())
		event2.blacklist.add(my_user2)
		self.assertIn(my_user2, event2.blacklist.all())
		event2.blacklist.remove(my_user2)
		self.assertNotIn(my_user2, event2.blacklist.all())

		post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=my_user)
		post2 = Post.objects.create(content="post_content", publish_date="1995-01-01", author=my_user2)
		self.assertEquals(post.content, "post_content")
		self.assertEquals(post.publish_date, "1995-01-01")
		self.assertIs(post.author, my_user)
		self.assertNotIn(my_user2, post.likes.all())
		post.likes.add(my_user2)
		self.assertIn(my_user2, post.likes.all())

		event2.users.add(my_user2)
		self.assertIn(my_user2, event2.users.all())

		event2.posts.add(post)
		self.assertIn(post, event2.posts.all())
		self.assertNotIn(post2, event2.posts.all())


def create_event(author):
	event = Event.objects.create(author=author, name="EventName", description="EventDescription",
								 start_date="1995-01-01", end_date="1995-01-02", place_text="miejsce",
								 place_location_lat=1, place_location_lng=1)
	return event


def create_user():
	my_user = UserenaSignup.objects.create_user(username="my_name", email="my_name@gmail.com", password="my_password")
	return my_user

def create_user2():
	my_user = UserenaSignup.objects.create_user(username="my_name2", email="my_name2@gmail.com", password="my_password")
	return my_user

class EventDetailsViewTests(TestCase):
	def test_no_events(self):
		call_command('check_permissions')

		user = create_user()
		user.save()
		active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)

		active_user.save()
		event = create_event(active_user)
		event.save()
		self.client.login(username=active_user.username, password="my_password", email= active_user.email)
		response = self.client.get(reverse('events:details', args=(event.pk,)))
		self.assertEqual(response.request['PATH_INFO'], '/events/show/1/')
		self.assertEqual(response.status_code, 200)

class ObserveEventTests(TestCase):
	def test(self):
		call_command('check_permissions')
		user = create_user()
		user.save()
		user2 = create_user2()

		active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)

		active_user.save()
		event = create_event(active_user)
		event.save()
		self.client.login(username=active_user.username, password="my_password", email= active_user.email)
		user2.my_profile.observing_events.add(event)
		self.assertIn(event,user2.my_profile.observing_events.all())
		self.assertNotIn(event,user.my_profile.observing_events.all())



class EventDestroyViewTests(TestCase):
	def test_destroy(self):
		call_command('check_permissions')

		user = create_user()
		user.save()
		active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)

		active_user.save()

		event = create_event(active_user)
		event.author = active_user
		event.save()
		self.client.login(username=active_user.username, password="my_password", email=active_user.email)
		response = self.client.post(reverse('events:destroy', args=(event.pk,)))
		self.assertEqual(response.request['PATH_INFO'], '/events/destroy/1/')
		self.assertEqual(response.status_code, 302)



	def test_user_is_not_author(self):
		call_command('check_permissions')
		user = create_user()
		user.save()
		active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)

		active_user.save()

		user2 = create_user2()
		user2.save()
		active_user2 = UserenaSignup.objects.activate_user(user2.userena_signup.activation_key)

		active_user2.save()

		event = create_event(active_user)
		event.author = active_user
		event.save()
		self.client.login(username=active_user2.username, password="my_password", email=active_user2.email)
		response = self.client.post(reverse('events:destroy', args=(event.pk,)))
		self.assertEqual(response.status_code, 302)


class EventViewTests(TestCase):
	def test_on_views1_niezalogowany(self):
		call_command('check_permissions')

		user = create_user()
		user.save()
		active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)

		active_user.save()
		event = create_event(active_user)
		event.save()

		client = Client()

		response = self.client.get(reverse('events:details', args=(event.pk, )))
		self.assertEqual(response.status_code, 302)

		response = self.client.get(reverse('events:index'))
		self.assertEqual(response.status_code, 302)

		response = self.client.get(reverse('events:create'))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:observe', args=[1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:like', args=[1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:unlike', args=[1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:block', args=[1, 1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:unblock', args=[1, 1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:leave', args=[1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:stop_observing', args=[1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:observe', args=[1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:join', args=[1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:destroy', args=[1, ]))
		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('events:observing'))
		self.assertEqual(response.status_code, 302)

		"""logujemy uzytkownika"""


class EventViewTests2(TestCase):
	def test_on_views1_zalogowany(self):
		call_command('check_permissions')

		user2 = create_user()
		user2.save()
		active_user2 = UserenaSignup.objects.activate_user(user2.userena_signup.activation_key)

		active_user2.save()
		event = create_event(active_user2)
		event.save()

		self.client.login(username=active_user2.username, password="my_password", email=active_user2.email)

		response = self.client.get(reverse('events:details', args=(event.pk, )))
		self.assertEqual(response.status_code, 200)

		response = self.client.get(reverse('events:index'))
		self.assertEqual(response.status_code, 200)

		response = self.client.get(reverse('events:create'))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:observe', args=[1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:like', args=[1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:unlike', args=[1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:block', args=[1, 1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:unblock', args=[1, 1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:leave', args=[1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:stop_observing', args=[1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:observe', args=[1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:join', args=[1, ]))
		self.assertEqual(response.status_code, 200)

		response = self.client.post(reverse('events:observing'))
		self.assertEqual(response.status_code, 200)


		response = self.client.get('/accounts/signout/', follow=True)
		self.assertRedirects(response, '/')


		response = self.client.get('/accounts/signout/', follow=True)
		self.assertRedirects(response, '/')
