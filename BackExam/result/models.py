from django.db import models
from designexam.models import Exam


class Result(models.Model):
    exam = models.ForeignKey(Exam, null=False, on_delete=models.CASCADE)
    score = models.FloatField(null=False)
    types = (('Descriptive', 'Descriptive'), ('Multiple', 'Multiple'))
    question_type = models.CharField(choices=types, null=True)
    

