from django.db import models

class GolferMatch(models.Model):
    golfer=models.ForeignKey('Golfer', on_delete=models.CASCADE)
    match=models.ForeignKey('Match', on_delete=models.CASCADE)
