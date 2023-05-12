from django.db import models

class HoleScore(models.Model):
    golfer_match=models.ForeignKey('GolferMatch', on_delete=models.CASCADE, related_name='scores')
    strokes=models.IntegerField()
    course_hole=models.IntegerField()
    notes=models.CharField(max_length=50)
