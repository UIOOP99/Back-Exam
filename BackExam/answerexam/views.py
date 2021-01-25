from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from .serializers import DescriptiveAnswerSerializer, MultipleAnswerSerializer, DescriptiveFileSerializer
from designexam.models import Exam, DescriptiveQuestion, MultipleQuestion
# Create your views here.
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DescriptiveAnswer, MultipleAnswer
from client_process.file_management import retrieve_file
# from operator import attrgetter
from itertools import chain
from account.models import User

class DescriptiveAnswerViewSet(ModelViewSet):
    serializer_class = DescriptiveAnswerSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = DescriptiveAnswer.objects.all()
    http_method_names = ['get', 'post']

    # PERMISSIONS SHOULD BE WRITEN

    # swagger should be added
    def create(self, request, *args, **kwargs):
        try:
            des_que = DescriptiveQuestion.objects.get(pk=request.data['descriptive_questionID'])
        except DescriptiveQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data, descriptive_que_id=request.data['descriptive_questionID'])
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # swagger should be added
    def perform_create(self, serializer):
        answer = serializer.save()
        answer.save()
        serializer.save()

    # swagger should be added
    @action(detail=True, methods=['post'])
    def create_file(self, request, pk):
        try:
            des_answer = DescriptiveAnswer.objects.get(pk=pk)
        except DescriptiveAnswer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_serializer = DescriptiveFileSerializer(data=request.data,
                                                    descriptive_answer_id=pk,
                                                    descriptive_que_id=des_answer.descriptive_questionID.pk
                                                    )
        if file_serializer.is_valid():
            file_serializer.update_instance()
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # swagger should be added
    @action(detail=True, methods=['get'])
    def get_file_url(self, request, pk):
        try:
            des_answer = DescriptiveAnswer.objects.get(pk=pk)
        except DescriptiveAnswer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # if des_answer have file:
        result = retrieve_file(des_answer.file_id)
        return Response(data={'url': result}, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_404_NOT_FOUND)


class MultipleAnswerViewSet(ModelViewSet):
    serializer_class = MultipleAnswerSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = DescriptiveAnswer.objects.all()
    http_method_names = ['post']

    # PERMISSIONS SHOULD BE WRITEN

    # swagger should be added
    def create(self, request, *args, **kwargs):
        try:
            mul_que = MultipleQuestion.objects.get(pk=request.data['multiple_questionID'])
        except MultipleQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data,
                                         multiple_que_id=request.data['multiple_questionID']
                                         )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # swagger should be added
    def perform_create(self, serializer):
        answer = serializer.save()
        answer.save()
        serializer.save()


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def answers_list(request, examID, studentID):
    try:
        exam = Exam.objects.get(pk=examID)
        student = User.objects.get(pk=studentID)
        que_list = DescriptiveQuestion.objects.filter(examID=examID).values_list('id', flat=True)
        a1 = MultipleAnswer.objects.filter(multiple_questionID__in=que_list, studentID=student).values('pk', 'multiple_questionID',
                                                                                               'studentID',
                                                                                               'answer_choice',
                                                                                               'created_date')
        a2 = DescriptiveAnswer.objects.filter(descriptive_questionID__in=que_list, studentID=student).values('pk', 'descriptive_questionID',
                                                                                            'text', 'file_id',
                                                                                            'studentID', 'created_date')
        result_list = list(chain(a1, a2))
        return Response(data={'list': result_list}, status=status.HTTP_200_OK)
    except Exam.DoesNotExist or User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def answers_list2(request, examID):
    try:
        exam = Exam.objects.get(pk=examID)
        que_list = DescriptiveQuestion.objects.filter(examID=examID).values_list('id', flat=True)
        a1 = MultipleAnswer.objects.filter(multiple_questionID__in=que_list).values('pk', 'multiple_questionID', 'studentID',
                                                                          'answer_choice',
                                                                          'created_date')
        a2 = DescriptiveAnswer.objects.filter(descriptive_questionID__in=que_list).values('pk', 'descriptive_questionID',
                                                                       'text', 'file_id',
                                                                       'studentID', 'created_date')
        result_list = list(chain(a1, a2))
        return Response(data={'list': result_list}, status=status.HTTP_200_OK)
    except Exam.DoesNotExist or User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)