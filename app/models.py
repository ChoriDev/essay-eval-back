from django.db import models

class Essay(models.Model):
    content = models.CharField(max_length=1000)
    feedback = models.TextField(default="")