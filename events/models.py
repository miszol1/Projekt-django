from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from taggit.managers import TaggableManager

# https://docs.djangoproject.com/en/1.11/ref/models/fields/#manytomany-arguments
# https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/


class Event(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=4000, blank=False)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    place_text = models.CharField(max_length=80, blank=False)
    place_location_lat = models.FloatField(blank=False)
    place_location_lng = models.FloatField(blank=False)
    users = models.ManyToManyField(User)
    posts = models.ManyToManyField(Post)
    author = models.ForeignKey(User, related_name="autor")
    tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, related_name="likes")
    blacklist = models.ManyToManyField(User, related_name="blacklist")

    def __str__(self):
        return self.name


"""
class EventUser(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
"""
