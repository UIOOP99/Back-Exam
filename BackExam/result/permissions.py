from rest_framework import permissions
import datetime

from .models import Result
from .utility.answer_obj_checker import is_exist_answer, get_exam_obj
from designexam.models import Exam
from client_process.get_classes import get_classes

class HasCreateAccess(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.role == "STUDENT":
            return False

        elif request.user.role == 'PROFESSOR':
            exam = get_exam_obj(request.data['answer_id'], request.data['question_type'])
            if exam is None:
                return False
            courses = get_classes(request.user.id)
            if exam.courseID not in courses:
                return False

        return True

class HasUpdateDeleteAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "STUDENT":
            return False
        try:
            result = Result.objects.get(pk=view.kwargs['pk'])
        except Result.DoesNotExist:
            return False

        elif request.user.role == 'PROFESSOR':
            exam = get_exam_obj(result.answer_id, result.question_type)
            if exam is None:
                return False
            courses = get_classes(request.user.id)
            if exam.courseID not in courses:
                return False

        return True


class HasReadAccess(permissions.BasePermission):

    def has_permission(self, request, view):

        try:
            result = Result.objects.get(pk=view.kwargs['pk'])
        except Result.DoesNotExist:
            return False

        if request.user.role == 'PROFESSOR':
            exam = get_exam_obj(result.answer_id, result.question_type)
            if exam is None:
                return False
            courses = get_classes(request.user.id)
            if exam.courseID not in courses:
                return False

        elif request.user.role == 'STUDENT':
            answer = is_exist_answer(result.answer_id, result.question_type)
            if answer is None:
                return False
            if answer.studentID.id != request.user.id:
                return False

        return True


class HasResultsExamAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.user.role == 'STUDENT':
            return False
        
        try:
            exam = Exam.objects.get(pk=view.kwargs['exam_id'])
        except Exam.DoesNotExist:
            return False

        elif request.user.role == 'PROFESSOR':
            courses = get_classes(request.user.id)
            if exam.courseID not in courses:
                return False

        return True
        

class HasResultsStudentAccess(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.role == 'PROFESSOR':
            return False
        
        elif request.user.role == "STUDENT":
            if request.user.id != view.kwargs['student_id']
                return False

        return True
        



