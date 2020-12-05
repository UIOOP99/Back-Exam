from rest_framework import permissions
from client_process.get_classes import get_classes
import datetime
from .models import Exam


class IsOwnerToCreate(permissions.BasePermission):
    # check this id is the teacher of the class
    def has_permission(self, request, view):
        classes = get_classes(request.user.id)
        if request.data['courseID'] not in classes:
            return False
        return True


class IsOwnerToEditDelete(permissions.BasePermission):
    # check this id is the teacher of the class
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        classes = get_classes(request.user.id)
        if exam.courseID not in classes:
            return False

        return True


class HasTimeToEditDelete(permissions.BasePermission):
    #check the endtime 
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        if exam.end_date >= datetime.datetime.now():
            return False
        
        return True


class HasAccessToDelete(permissions.BasePermission):
    #check the author of exam for delete
    def has_permission(self, request, view):
        try:
            exam = Exam.objects.get(pk=view.kwargs['pk'])
        except Exam.DoesNotExist:
            return False

        if exam.author != 1:# must check the role and if he is teacher --> false
            return False
        
        return True

class HasAccessToEdit(permissions.BasePermission):
    #check has access to edit some fields
    def has_permission(self, request, view):
        pass


        


        
        
