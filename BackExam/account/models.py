from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    password = None
    first_name = None
    last_name = None
    email = None
    groups = None
    date_joined = None
    last_login = None
    role_choices = (('PROFESSOR', 'PROFESSOR'), ('ADMIN', 'ADMIN'), ('STUDENT', 'STUDENT'))
    id = models.PositiveIntegerField(primary_key=True, null=False)
    role = models.CharField(max_length=10, null=False, choices=role_choices)
