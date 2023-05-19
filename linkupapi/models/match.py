from django.db import models
from datetime import date, time
from django.utils.timezone import now   
class Match(models.Model):
    creator=models.ForeignKey("Golfer", on_delete=models.CASCADE, related_name='created_matches')
    golfers=models.ManyToManyField('Golfer', through='GolferMatch', related_name='my_matches')
    course=models.ForeignKey("Course", on_delete=models.CASCADE, related_name='matches')
    date=models.DateField(null=False, auto_now=False, auto_now_add=False, default=date.today)
    time=models.TimeField(null=False, auto_now=False, auto_now_add=False, default=now)
    message=models.CharField(max_length=50, null=True, blank=True)
    @property
    def joined(self):
        return self.__joined
    @joined.setter
    def joined(self, value):
        self.__joined = value