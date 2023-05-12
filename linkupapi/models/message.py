from django.db import models

class Message(models.Model):
    sender=models.ForeignKey('Golfer', on_delete=models.CASCADE, related_name='sent_messages')
    recipient=models.ForeignKey('Golfer', on_delete=models.CASCADE, related_name='received_messages')
    message=models.CharField(max_length=200)
    date_time=models.DateTimeField(auto_now=True)
    read=models.BooleanField()
