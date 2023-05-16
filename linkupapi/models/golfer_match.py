from django.db import models

class GolferMatch(models.Model):
    golfer=models.ForeignKey('Golfer', on_delete=models.CASCADE, related_name='matches')
    match=models.ForeignKey('Match', on_delete=models.CASCADE, related_name='players')
    is_initiator=models.BooleanField()