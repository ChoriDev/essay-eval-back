from django.db import models

class Essay(models.Model):
    essayContent = models.CharField(max_length=1000)

class Feedback(models.Model):
    feedbackContent = models.TextField(default="")