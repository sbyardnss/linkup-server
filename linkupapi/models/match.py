from django.db import models

class Match(models.Model):
    creator=models.ForeignKey("Golfer", on_delete=models.CASCADE, related_name='created_matches')
    # golfers=models.ManyToManyField('Golfer', through='GolferMatch', related_name='matches')
    course=models.ForeignKey("Course", on_delete=models.CASCADE, related_name='matches')
    date_time=models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    message=models.CharField(max_length=50)