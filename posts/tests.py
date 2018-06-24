# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
from django.test import TestCase
from userena.models import *
from .models import *
from accounts.models import *
from django.contrib.auth.models import Permission
from django.core.management import call_command
import logging
from django.core.urlresolvers import reverse

class PostTestCase(TestCase):
    def setUp(self):
        call_command('check_permissions')
        self.my_user = UserenaSignup.objects.create_user(username="my_name", email="my_name@gmail.com", password="my_password")
        self.my_user.save()
        self.my_user2 = UserenaSignup.objects.create_user(username="my_namee", email="my_name@gmail.com", password="my_password")
        self.my_user2.save()
        self.post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=self.my_user)
        self.comment = Comment.objects.create(content="comment_content", publish_date="1999-01-01", author=self.my_user2)


    def test_create(self):
        self.assertEquals(self.post.content, "post_content")
        self.assertEquals(self.post.publish_date, "1995-01-01")
        self.assertIs(self.post.author, self.my_user)

    def test_like(self):
        self.assertNotIn(self.my_user2, self.post.likes.all())
        self.post.likes.add(self.my_user2)
        self.assertIn(self.my_user2, self.post.likes.all())

    def test_createcomment(self):
        self.assertEquals(self.comment.content, "comment_content")
        self.assertEquals(self.comment.publish_date, "1999-01-01")
        self.assertIs(self.comment.author, self.my_user2)
        self.assertNotIn(self.comment, self.post.comments.all())
        self.post.comments.add(self.comment)
        self.assertIn(self.comment, self.post.comments.all())

def create_post(author):
	post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=author)
	return post

def create_event(author):
	event = Event.objects.create(author=author,name="EventName", description="EventDescription", start_date="1995-01-01", end_date="1995-01-02",place_text="miejsce",place_location_lat=1,place_location_lng=1)
	return event

def create_user():
	my_user = UserenaSignup.objects.create_user(username="my_name", email="my_name@gmail.com", password="my_password")
	return my_user;

class PostViewTests(TestCase):
    def test_post_details(self):
        call_command('check_permissions')

        user = create_user()
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()

        event = create_event(active_user)
        event.save()

        post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=active_user)
        post.save()

        event.posts.add(post)

        self.client.login(username=active_user.username, password="my_password", email= active_user.email)
        response = self.client.get(reverse('posts:details', args=(post.pk,event.pk,)))
        self.assertEqual(response.request['PATH_INFO'], '/posts/show/1/1/')
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        call_command('check_permissions')

        user = create_user()
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()

        event = create_event(active_user)
        event.save()
        self.client.login(username=active_user.username, password="my_password", email= active_user.email)
        response = self.client.post(reverse('posts:create', args=(event.pk,)))
        self.assertEqual(response.request['PATH_INFO'], '/posts/create/1/')
        self.assertEqual(response.status_code, 200)

    def test_create_post_comment(self):
        call_command('check_permissions')

        user = create_user()
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()

        event = create_event(active_user)
        event.save()

        post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=active_user)
        post.save()

        event.posts.add(post)

        self.client.login(username=active_user.username, password="my_password", email= active_user.email)
        response = self.client.post(reverse('posts:createcomment', args=(post.pk,event.pk,)))
        self.assertEqual(response.request['PATH_INFO'], '/posts/createcomment/1/1/')
        self.assertEqual(response.status_code, 200)

    def test_destroy_post(self):
        call_command('check_permissions')

        user = create_user()
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()

        event = create_event(active_user)
        event.save()

        post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=active_user)
        post.save()

        self.client.login(username=active_user.username, password="my_password", email= active_user.email)
        response = self.client.post(reverse('posts:destroy', args=(post.pk,event.pk,)))
        self.assertEqual(response.request['PATH_INFO'], '/posts/destroy/1/1/')
        self.assertEqual(response.status_code, 302)

    def test_destroy_post(self):
        call_command('check_permissions')

        user = create_user()
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()

        event = create_event(active_user)
        event.save()

        post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=active_user)
        post.save()
        comment = Comment.objects.create(content="comment_content", publish_date="1999-01-01", author=active_user)
        comment.save()

        self.client.login(username=active_user.username, password="my_password", email= active_user.email)
        response = self.client.post(reverse('posts:destroycomment', args=(post.pk,event.pk,comment.pk,)))
        self.assertEqual(response.request['PATH_INFO'], '/posts/destroycomment/1/1/1/')
        self.assertEqual(response.status_code, 302)

    def test_like_post(self):
        call_command('check_permissions')

        user = create_user()
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()

        event = create_event(active_user)
        event.save()

        post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=active_user)
        post.save()

        self.client.login(username=active_user.username, password="my_password", email= active_user.email)
        response = self.client.post(reverse('posts:like', args=(post.pk,event.pk,)))
        self.assertEqual(response.request['PATH_INFO'], '/posts/like/1/1/')
        self.assertEqual(response.status_code, 200)

    def test_unlike_post(self):
        call_command('check_permissions')

        user = create_user()
        user.save()
        active_user = UserenaSignup.objects.activate_user(user.userena_signup.activation_key)
        active_user.save()

        event = create_event(active_user)
        event.save()

        post = Post.objects.create(content="post_content", publish_date="1995-01-01", author=active_user)
        post.save()

        self.client.login(username=active_user.username, password="my_password", email= active_user.email)
        response = self.client.post(reverse('posts:unlike', args=(post.pk,event.pk,)))
        self.assertEqual(response.request['PATH_INFO'], '/posts/unlike/1/1/')
        self.assertEqual(response.status_code, 200)
