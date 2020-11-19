from django.db import models

# Create your models here.


class Exam(models.Model):  # Teachers
    title = models.CharField(max_length=200, blank=False, default='')
    courseID = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    duration = models.PositiveIntegerField()
    end_date = models.DateTimeField()
    have_file = models.BooleanField(default=False)  # Have a file containing all the questions
    file_URL = models.URLField(default=None)
    setting = models.BooleanField(default=True)  # True for FIX questions and False for RANDOM questions
    created_date = models.DateTimeField(auto_now_add=True, blank=False)


class DescriptiveQuestion(models.Model):  # Teachers
    examID = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False)
    text = models.TextField()
    mark = models.FloatField(default=0, blank=False)
    setting = models.BooleanField(default=True)  # if the teacher allows students to send files
    number = models.IntegerField(unique=True)


class MultipleQuestion(models.Model):  # Teachers
    examID = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False)
    text = models.TextField(default=False)
    mark = models.FloatField(default=0, blank=False)
    number = models.IntegerField(unique=True)
    answer = models.CharField(max_length=10)  # string of 0 & 1 that 0 is for False and 1 is for True
    options_text = models.JSONField()  # the text of each option


class DescriptiveQuestionFile(models.Model):  # Teachers
    descriptive_questionID = models.ForeignKey(DescriptiveQuestion, on_delete=models.CASCADE, blank=False)
    file_URL = models.URLField(default=None)


class MultipleQuestionFile(models.Model):  # Teachers
    multiple_questionID = models.ForeignKey(MultipleQuestion, on_delete=models.CASCADE, blank=False)
    file_URL = models.URLField(default=None)
