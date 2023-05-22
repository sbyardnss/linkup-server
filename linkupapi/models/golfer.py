from django.db import models
from django.contrib.auth.models import User

class Golfer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('Golfer', related_name='followers')
    matches = models.ManyToManyField('Match', related_name='players')
    @property
    def full_name(self):
        """full name custom property"""
        return f'{self.user.first_name} {self.user.last_name}'
    @property
    def email(self):
        return self.user.email
    @property
    def username(self):
        return self.user.username
    @property
    def password(self):
        return self.user.password
    @property
    def is_friend(self):
        return self.__is_friend
    @is_friend.setter
    def is_friend(self, value):
        self.__is_friend = value