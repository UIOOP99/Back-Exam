from django.db import models


class Result(models.Model):
    answer_id = models.PositiveIntegerField(null=False)
    mark = models.FloatField(null=False)
    types = (('Descriptive', 'Descriptive'), ('Multiple', 'Multiple'))
    question_type = models.CharField(choices=types, null=False)
