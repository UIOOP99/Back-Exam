from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Exam
from account.models import User
from .serializers import ExamSerializer, ExamFileSerializer, ExamListSerializer
from .permisions import IsOwnerToCreate, IsOwnerToEditDelete, HasAccessToDelete, HasAccessToEdit, \
    HasAccessToReadExams, HasTimeToEditDelete, ReachTimeToReadExam
from client_process.file_management import delete_file, retrieve_file
from client_process.get_classes import is_exist
from .exam_extra_classes.exam_list import ExamList, CourseExamList


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    http_method_names = ['get', 'delete', 'patch', 'post']
    
    def get_permissions(self):
        if self.action == "create" or self.action == "create_file":
            permission = [IsAuthenticated, IsOwnerToCreate, ]

        elif self.action == "partial_update":
            permission = [IsAuthenticated, IsOwnerToEditDelete, HasTimeToEditDelete, HasAccessToEdit, ]
        
        elif self.action == "destroy" or self.action == "delete_file":
            permission = [IsAuthenticated, IsOwnerToEditDelete, HasTimeToEditDelete, HasAccessToDelete, ]
        
        elif self.action == "retrieve" or self.action == "get_file_url":
            permission = [IsAuthenticated, HasAccessToReadExams, ReachTimeToReadExam, ]
        
        else:
            permission = [IsAuthenticated, HasAccessToReadExams, ]
        
        return permission
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, user_id):
        user_role = User.objects.get(pk=user_id).role
        serializer.author = user_role
        serializer.save()

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def create_file(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_serializer = ExamFileSerializer(id=pk)
        if file_serializer.is_valid():
            file_serializer.update_instance()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def delete_file(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        delete_file(pk)
        exam.have_file = False
        exam.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    @action(detail=True, methods=['get'])
    def get_file_url(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        result = retrieve_file(pk)
        return Response(data={'url': result}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_exams(self, request):
        exams = ExamList(request.user.id).get_exams()
        exams_ser = ExamListSerializer(exams, many=True)
        return Response(exams_ser.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, HasAccessToReadExams))
def get_course_exams(self, request, course_id):
    if not is_exist(course_id):
        return Response(status=status.HTTP_404_NOT_FOUND)
    exams = CourseExamList(course_id).get_exams
    exam_ser = ExamListSerializer(exams, many=True)
    return Response(exam_ser.data, status=status.HTTP_200_OK)
    
    

    
