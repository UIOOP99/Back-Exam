from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Exam
from .serializers import ExamSerializer, ExamFileSerializer
from client_process.file_management import delete_file, retrieve_file


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    http_method_names = ['get', 'delete', 'patch', 'post']
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request.auth.payload['role']['Name'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, role_name):
        if role_name == 'admin':
            serializer.author = 2
        elif role_name == 'professor':
            serializer.author = 1
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
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    @action(detail=True, methods=['get'])
    def get_file_url(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        result = retrieve_file(pk)
        return Response(data={'url': result.url}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_exams(self, request):
        pass
    

    
