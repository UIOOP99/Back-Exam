from rest_framework import permissions
import datetime
from django.utils import timezone

from client_process.get_classes import get_classes
from designexam.models import Exam, DescriptiveQuestion, MultipleQuestion
from account.models import User


class IsOwnerToCreateMultipleQueAns(permissions.BasePermission):
    def has_permission(self, request, view):
        exam = MultipleQuestion.objects.get(pk=request.data['multiple_questionID']).examID
        if request.user.role == "STUDENT" and exam.end_date < timezone.now():
            classes = get_classes(request.user.id)
            course_id = exam.courseID
            if course_id not in classes:
                return False
            else:
                return True
        else:
            return False


class IsOwnerToCreateDescriptiveQueAns(permissions.BasePermission):
    def has_permission(self, request, view):
        exam = DescriptiveQuestion.objects.get(pk=request.data['descriptive_questionID']).examID
        if request.user.role == "STUDENT" and exam.end_date < timezone.now():
            classes = get_classes(request.user.id)
            course_id = exam.courseID
            if course_id not in classes:
                return False
            else:
                return True
        else:
            return False

