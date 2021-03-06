from django.db import models


class Exam(models.Model):  # Teachers
    title = models.CharField(max_length=200, blank=False, default='')
    courseID = models.CharField(max_length=200, null=False)
    description = models.TextField()
    start_date = models.DateTimeField(null=False)
    #duration = models.PositiveIntegerField()
    end_date = models.DateTimeField(null=False)
    have_file = models.BooleanField(default=False)  # Have a file containing all the questions
    file_id = models.PositiveIntegerField(default=None, null=True)
    setting = models.BooleanField(default=True)  # True for FIX questions and False for RANDOM questions
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    author_choices = (('PROFESSOR', 'PROFESSOR'), ('ADMIN', 'ADMIN'), )
    author = models.CharField(max_length=10, null=True, choices=author_choices)


class DescriptiveQuestion(models.Model):  # Teachers
    examID = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False)
    text = models.TextField()
    mark = models.FloatField(default=0, blank=False)
    setting = models.BooleanField(default=True)  # if the teacher allows students to send files
    number = models.IntegerField(unique=True)


class MultipleQuestion(models.Model):  # Teachers
    examID = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False)
    text = models.TextField()
    mark = models.FloatField(default=0, blank=False)
    number = models.IntegerField(unique=True)
    answer = models.CharField(max_length=10)  # string of 0 & 1 that 0 is for False and 1 is for True
    options_text = models.TextField() # the text of each option


class DescriptiveQuestionFile(models.Model):  # Teachers
    descriptive_questionID = models.ForeignKey(DescriptiveQuestion, on_delete=models.CASCADE, blank=False)
    file_id = models.PositiveIntegerField(default=None, null=True)


class MultipleQuestionFile(models.Model):  # Teachers
    multiple_questionID = models.ForeignKey(MultipleQuestion, on_delete=models.CASCADE, blank=False)
    file_id = models.PositiveIntegerField(default=None, null=True)
