from django.db import models

class Essay(models.Model):
    original_text = models.CharField(max_length=1000)
    corrected_text = models.TextField(default="")
    wrong_spelling = models.JSONField(default=list)
    wrong_spacing = models.JSONField(default=list)