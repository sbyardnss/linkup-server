from django.db import models
from linkupapi.models import Golfer
class HoleScore(models.Model):
    golfer=models.ForeignKey(Golfer, on_delete=models.CASCADE, default=1, related_name='my_scores')
    match = models.ForeignKey('Match', on_delete=models.CASCADE, default=1, related_name='all_player_scores')
    strokes=models.IntegerField()
    course_hole=models.IntegerField()
    notes=models.CharField(max_length=50, blank=True)
