from django.db import models

class Essay(models.Model):
    original_text = models.CharField(max_length=1000)
    corrected_text = models.TextField(default="")
    wrong_spelling = models.JSONField(default=list)
    wrong_spacing = models.JSONField(default=list)
    cont1_score = models.FloatField()
    cont1_comment = models.TextField(default="")
    cont2_score = models.FloatField()
    cont2_comment = models.TextField(default="")
    exp2_score = models.FloatField()
    exp2_comment = models.TextField(default="")
    exp3_score = models.FloatField()
    exp3_comment = models.TextField(default="")
    org3_score = models.FloatField()
    org3_comment = models.TextField(default="")