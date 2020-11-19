from django.db import models
from designexam.models import MultipleQuestion, DescriptiveQuestion


class MultipleAnswer(models.Model):  # Students
    multiple_questionID = models.ForeignKey(MultipleQuestion, on_delete=models.CASCADE, blank=False)
    studentID = models.CharField(max_length=200)
    answer_choice = models.CharField(max_length=10)  # string of 0 & 1 that 0 is for False and 1 is for True
    created_date = models.DateTimeField(auto_now_add=True, blank=False)


class DescriptiveAnswer(models.Model):  # Students
    descriptive_questionID = models.ForeignKey(DescriptiveQuestion, on_delete=models.CASCADE, blank=False)
    studentID = models.CharField(max_length=200)
    file_URL = models.URLField(default=None)  # if teacher allow them
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, blank=False)

