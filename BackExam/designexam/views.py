from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import transaction
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from operator import attrgetter
from itertools import chain

from .models import Exam, DescriptiveQuestion, MultipleQuestion,\
    DescriptiveQuestionFile, MultipleQuestionFile
from account.models import User
from .serializers import ExamSerializer, ExamFileSerializer, ExamListSerializer,\
    DescriptiveQuestionSerializer, DescriptiveQuestionFileSerializer,\
    MultipleQuestionSerializer, MultipleQuestionFileSerializer
    # MultipleQuestionListSerializer, DescriptiveQuestionListSerializer
from .permisions import IsOwnerToCreate, IsOwnerToEditDelete, HasAccessToDelete, HasAccessToEdit, \
    HasAccessToReadExam, HasTimeToEditDelete, ReachTimeToReadExam, HasAccessToReadExams
from client_process.file_management import delete_file, retrieve_file
from client_process.get_classes import is_exist
from .exam_extra_classes.exam_list import ExamList, CourseExamList


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ExamSerializer
    parser_classes = [FormParser, MultiPartParser]
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
        
    @swagger_auto_schema(tags=['exam'])
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
    cann't set start_date and end_date in request.body""")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Exam File'], operation_description="sould upload a file {'questions_file': FILE}", responses={201: ""},
    request_body=ExamFileSerializer)
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
    

class DescriptiveQuestionViewSet(ModelViewSet):
    serializer_class = DescriptiveQuestionSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = DescriptiveQuestion.objects.all()
    http_method_names = ['get', 'post']

    # PERMISSIONS SHOULD BE WRITEN

    # swagger should be added
    def create(self, request, *args, **kwargs):
        try:
            exam = Exam.objects.get(pk=request.data['examID'])
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data, examID=request.data['examID'])
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # swagger should be added
    def perform_create(self, serializer):
        des_question = serializer.save()
        des_question.save()
        # serializer.save()

    # swagger should be added
    @action(detail=True, methods=['post'])
    def create_file(self, request, pk):
        try:
            des_que= DescriptiveQuestion.objects.get(pk=pk)
        except DescriptiveQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_serializer = DescriptiveQuestionFileSerializer(data=request.data,
                                                            descriptive_que_id=pk)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # swagger should be added
    @action(detail=True, methods=['get'])
    def get_file_url(self, request, pk):
        try:
            des_que = DescriptiveQuestion.objects.get(pk=pk)
        except DescriptiveQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            que_files_list= DescriptiveQuestionFile.objects.filter(
                descriptive_questionID=pk).values_list('file_id', flat=True)
            result = []
            for a in que_files_list:
                result.append(retrieve_file(a))
            return Response(data={'url': result}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MultipleQuestionViewSet(ModelViewSet):
    serializer_class = MultipleQuestionSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = MultipleQuestion.objects.all()
    http_method_names = ['get', 'post']

    # PERMISSIONS SHOULD BE WRITEN

    # swagger should be added
    def create(self, request, *args, **kwargs):
        try:
            exam = Exam.objects.get(pk=request.data['examID'])
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data, examID=request.data['examID'])
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # swagger should be added
    def perform_create(self, serializer):
        mul_question = serializer.save()
        mul_question.save()
        # serializer.save()

    # swagger should be added
    @action(detail=True, methods=['post'])
    def create_file(self, request, pk):
        try:
            mul_que= MultipleQuestion.objects.get(pk=pk)
        except MultipleQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_serializer = MultipleQuestionFileSerializer(data=request.data,
                                                         multiple_que_id=pk)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # swagger should be added
    @action(detail=True, methods=['get'])
    def get_file_url(self, request, pk):
        try:
            mul_que = MultipleQuestion.objects.get(pk=pk)
        except MultipleQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            mul_files_list = MultipleQuestionFile.objects.filter(
                multiple_questionID=pk).values_list('file_id', flat=True)
            result = []
            for a in mul_files_list:
                result.append(retrieve_file(a))
            return Response(data={'url': result}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def  questions_list(request, pk):
    q1 = MultipleQuestion.objects.filter(examID=pk).values('pk', 'examID', 'text', 'mark', 'number', 'answer', 'options_text')
    q2 = DescriptiveQuestion.objects.filter(examID=pk).values('pk', 'examID', 'text', 'mark', 'number', 'setting')
    result_list = list(chain(q1, q2))
    return Response(data={'list': result_list}, status=status.HTTP_200_OK)

''''
class DescriptiveQuestions(ListAPIView):
    serializer_class = DescriptiveQuestionListSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        # try:
        #     exam_pk = kwargs['pk']
        #     exam = Exam.objects.get(pk=exam_pk)
        ques = DescriptiveQuestion.objects.filter(examID=kwargs['pk'])
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(ques, request)
        desques_ser = DescriptiveQuestionListSerializer(result_page, many=True)
        return paginator.get_paginated_response(desques_ser.data)
        # except Exam.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)


class MultipleQuestions(ListAPIView):
    serializer_class = MultipleQuestionListSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        try:
            exam_pk = kwargs['pk']
            exam = Exam.objects.get(pk=exam_pk)
            ques = MultipleQuestion.objects.filter(examID=exam_pk)
            paginator = PageNumberPagination()
            paginator.page_size = 20
            result_page = paginator.paginate_queryset(ques, request)
            mulques_ser = MultipleQuestionListSerializer(result_page, many=True)
            return paginator.get_paginated_response(mulques_ser.data)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

'''''