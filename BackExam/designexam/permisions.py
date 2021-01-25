from rest_framework import permissions
import datetime
from django.utils import timezone

from client_process.get_classes import get_classes
from .models import Exam
from account.models import User


class IsOwnerToCreate(permissions.BasePermission):
    # check this id is the teacher of the class or it is admin
    def has_permission(self, request, view):
        if request.user.role == "ADMIN":
            return True
        elif request.user.role == "PROFESSOR":
            classes = get_classes(request.user.id)
            if request.data['courseID'] not in classes:
                return False
            return True
        return False


class IsOwnerToEditDelete(permissions.BasePermission):
    # check this id is the teacher of the class or it is admin
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        if request.user.role == "ADMIN":
            return True
        elif request.user.role == "PROFESSOR":
            classes = get_classes(request.user.id)
            if exam.courseID not in classes:
                return False
            return True

        return False


class HasTimeToEditDelete(permissions.BasePermission):
    #check the endtime 
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        if request.user.role == "ADMIN":
            return True

        if exam.end_date <= timezone.now():
            return False
        
        return True


class HasAccessToDelete(permissions.BasePermission):
    #check the author of exam for delete
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        if exam.author == "ADMIN" and request.user.role == "PROFESSOR":
            return False
        
        return True

class HasAccessToEdit(permissions.BasePermission):
    #check has access to edit some fields
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        if request.user.role == "PROFESSOR" and\
            ("start_date" in request.data or "end_date" in request.data):
            return False
        
        return True


class HasAccessToReadExam(permissions.BasePermission):
    #check the user has access to see more details about exam
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        if request.user.role == "ADMIN":
            return True
        else:
            classes = get_classes(request.user.id)
            if exam.courseID not in classes:
                return False
        
        return True


class HasAccessToReadExams(permissions.BasePermission):
    #check the user has access to see more details about exam
    def has_permission(self, request, view):
        if request.user.role == "ADMIN":
            return True
        else:
            classes = get_classes(request.user.id)
            if view.kwargs['course_id'] not in classes:
                return False
        
        return True


class ReachTimeToReadExam(permissions.BasePermission):
    #check the time for Student to see more details about exam
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        if request.user.role == "STUDENT":
            if exam.start_date > timezone.now():
                return False
        
        return True


class IsOwnerToCreateQue(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=request.data['examID'])
            if request.user.role == "PROFESSOR" and exam.end_date >= timezone.now():
                classes = get_classes(request.user.id)
                course_id = exam.courseID
                if course_id not in classes:
                    return False
                else:
                    return True
            else:
                return False
        except Exam.DoesNotExist:
            return False


class HasAccessToReadQues(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['examID'])
            if request.user.role == "PROFESSOR":
                classes = get_classes(request.user.id)
                if exam.courseID not in classes:
                    return False
                return True
            elif request.user.role == "ADMIN":
                return True
            elif request.user.role == "STUDENT" and exam.end_date >= timezone.now() >= exam.start_date():
                return True
            else:
                return False
        except Exam.DoesNotExist:
            return False


class IsOwnerToCreateFile(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk']).examID
            if request.user.role == "PROFESSOR" and exam.end_date >= timezone.now():
                classes = get_classes(request.user.id)
                course_id = exam.courseID
                if course_id not in classes:
                    return False
                else:
                    return True
            else:
                return False
        except Exam.DoesNotExist:
            return False