from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Exam
from .serializers import ExamSerializer


@api_view(['GET',])
@permission_classes((IsAuthenticated))
def get_classes(request):
    pass


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    http_method_names = ['get', 'delete', 'patch', 'post']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        pass

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

    def partial_update(self, request, *args, **kwargs):
        pass

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        pass
    

    
