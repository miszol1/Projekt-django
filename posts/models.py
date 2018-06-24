# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Comment(models.Model):
    content = models.TextField(max_length=4000, blank=False)
    publish_date = models.DateTimeField(blank=False)
    author = models.ForeignKey(User, related_name="authorcomment")


class Post(models.Model):
    content = models.TextField(max_length=4000, blank=False)
    publish_date = models.DateTimeField(blank=False)
    author = models.ForeignKey(User, related_name="autorpost")
    comments = models.ManyToManyField(Comment)
    likes = models.ManyToManyField(User)
