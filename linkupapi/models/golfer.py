from django.db import models
from django.contrib.auth.models import User

class Golfer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    @property
    def full_name(self):
        """full name custom property"""
        return f'{self.user.first_name} {self.user.last_name}'
