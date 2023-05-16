from django.db import models
from django.contrib.auth.models import User

class Friendship(models.Model):
    golfer = models.ForeignKey("Golfer", on_delete=models.CASCADE, related_name='my_friends')
    friend = models.ForeignKey("Golfer", on_delete=models.CASCADE, related_name='friendships')
    created_on = models.DateTimeField(auto_now=True)