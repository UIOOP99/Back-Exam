from django.db import models


class Result(models.Model):
    answer_id = models.PositiveIntegerField(null=False)
    mark = models.FloatField(null=False)
    types = (('Descriptive', 'Descriptive'), ('Multiple', 'Multiple'))
    question_type = models.CharField(choices=types, null=False, max_length=20)

    class Meta:
       unique_together = ('answer_id', 'question_type', )
       index_together = [
           ['answer_id', 'question_type', ]
       ]
