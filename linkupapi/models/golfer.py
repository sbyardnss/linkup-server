from django.db import models
from django.contrib.auth.models import User

class Golfer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('Golfer', related_name='followers')
    @property
    def full_name(self):
        """full name custom property"""
        return f'{self.user.first_name} {self.user.last_name}'
    @property
    def is_friend(self):
        return self.__is_friend
    @is_friend.setter
    def is_friend(self, value):
        self.__is_friend = value