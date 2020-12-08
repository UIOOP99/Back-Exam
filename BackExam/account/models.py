from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    password = None
    last_login = None
    role_choices = (('PROFESSOR', 'PROFESSOR'), ('ADMIN', 'ADMIN'), ('STUDENT', 'STUDENT'))
    id = models.PositiveIntegerField(primary_key=True, null=False)
    role = models.CharField(max_length=10, null=False, choices=role_choices)
    USERNAME_FIELD = 'id'
