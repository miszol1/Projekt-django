from django.db import models
from django.contrib.auth import get_user_model

class Reputation(models.Model):
    from_user = models.ForeignKey(get_user_model(), related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(get_user_model(), related_name="to_user", on_delete=models.CASCADE)
    time_added = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()
    description = models.CharField(max_length=200)
