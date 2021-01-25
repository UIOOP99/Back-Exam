from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .serializers import DescriptiveAnswerSerializer, MultipleAnswerSerializer, DescriptiveFileSerializer
from designexam.models import Exam, DescriptiveQuestion, MultipleQuestion
# Create your views here.
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DescriptiveAnswer, MultipleAnswer
from client_process.file_management import retrieve_file



class DescriptiveAnswerViewSet(ModelViewSet):
    serializer_class = DescriptiveAnswerSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = DescriptiveAnswer.objects.all()
    http_method_names = ['get', 'post']

    # PERMISSIONS SHOULD BE WRITEN

    # swagger should be added
    def create(self, request, *args, **kwargs):
        try:
            des_que = DescriptiveQuestion.objects.get(pk=pk)
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
                                                    descriptive_que_id=request.data['descriptive_questionID']
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
            mul_que = MultipleQuestion.objects.get(pk=pk)
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
