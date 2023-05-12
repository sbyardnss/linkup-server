from django.db import models

class Course(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=25)
    url=models.CharField(max_length=300)