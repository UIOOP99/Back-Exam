from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.db import transaction
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.inspectors import DjangoRestResponsePagination

from .models import Exam
from account.models import User
from .serializers import ExamSerializer, ExamFileSerializer, ExamListSerializer
from .permisions import IsOwnerToCreate, IsOwnerToEditDelete, HasAccessToDelete, HasAccessToEdit, \
    HasAccessToReadExam, HasTimeToEditDelete, ReachTimeToReadExam, HasAccessToReadExams
from client_process.file_management import delete_file, retrieve_file
from client_process.get_classes import is_exist
from .exam_extra_classes.exam_list import ExamList, CourseExamList


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ExamSerializer
    http_method_names = ['get', 'delete', 'patch', 'post']
    
    def get_permissions(self):
        if self.action == "create":
            permission = (IsAuthenticated(), IsOwnerToCreate(), )

        elif self.action == "create_file":
            permission = (IsAuthenticated(), IsOwnerToEditDelete(), HasTimeToEditDelete(), )

        elif self.action == "partial_update":
            permission = (IsAuthenticated(), IsOwnerToEditDelete(), HasTimeToEditDelete(), HasAccessToEdit(), )
        
        elif self.action == "destroy" :
            permission = (IsAuthenticated(), IsOwnerToEditDelete(), HasTimeToEditDelete(), HasAccessToDelete(), )
        
        elif self.action == "delete_file":
            permission = (IsAuthenticated(), IsOwnerToEditDelete(), HasTimeToEditDelete(), )
        
        elif self.action == "retrieve" or self.action == "get_file_url":
            permission = (IsAuthenticated(), HasAccessToReadExam(), ReachTimeToReadExam(), )
        
        else:
            permission = (IsAuthenticated(), )
        
        return permission
        
    @swagger_auto_schema(tags=['exam'], responses={status.HTTP_400_BAD_REQUEST: """{
    "non_field_errors": ["this time have conflict with other exams"]} or\n
    {"start_date": [ "start date must be more than now"], "end_date": ["end date must be more than start time and now"]} or\n ...""",
    status.HTTP_403_FORBIDDEN: '{ "detail": "You do not have permission to perform this action."}',
    status.HTTP_201_CREATED: ExamSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request.user.role)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, user_role):
        exam = serializer.save()
        exam.author = user_role
        exam.save()
        serializer.author = user_role
        serializer.save()

    @swagger_auto_schema(tags=['exam'])
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=['exam'], 
    operation_description="""before the end_date can edit some fields. if the auther is ADMIN and the user.role is PROFESSOR, 
    cann't set start_date and end_date in request.body . respose format = response of create format""")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Exam File'], operation_description="sould upload a file {'questions_file': FILE}", 
    request_body=ExamFileSerializer, responses={status.HTTP_201_CREATED: "", status.HTTP_400_BAD_REQUEST: """{
    "questions_file": ["the format is invalid" or "the size of file is above of 10 MB" or this exam has questions]} """})
    @action(detail=True, methods=['post'])
    def create_file(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_serializer = ExamFileSerializer(data=request.data, exam_id=pk)
        if file_serializer.is_valid():
            file_serializer.update_instance()
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Exam File'], responses={404: "", 204:""})
    @action(detail=True, methods=['delete'])
    def delete_file(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if exam.have_file:
            result = delete_file(exam.file_id)
            exam.have_file = False
            exam.file_id = None
            exam.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(tags=['Exam File',], operation_description="get file exam URL", 
    responses={status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_OBJECT,properties={'url': openapi.Schema(type=openapi.TYPE_STRING)})})
    @action(detail=True, methods=['get'])
    def get_file_url(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if exam.have_file:
            result = retrieve_file(exam.file_id)
            return Response(data={'url': result}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    
class Exams(ListAPIView):
    serializer_class = ExamListSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        exams = ExamList(request.user.id).get_exams()
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(exams, request)
        exams_ser = ExamListSerializer(result_page, many=True)
        return paginator.get_paginated_response(exams_ser.data)


class CourseExams(ListAPIView):
    serializer_class = ExamListSerializer
    permission_classes = (IsAuthenticated, HasAccessToReadExams, )

    def list(self, request, *args, **kwargs):
        if not is_exist(kwargs['course_id']):
            return Response(status=status.HTTP_404_NOT_FOUND)
        exams = CourseExamList(kwargs['course_id']).get_exams()
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(exams, request)
        exams_ser = ExamListSerializer(result_page, many=True)
        return paginator.get_paginated_response(exams_ser.data)
    

    
