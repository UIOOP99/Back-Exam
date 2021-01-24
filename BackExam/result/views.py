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

from .models import Result
from account.models import User
from designexam.models import Exam
from .serializers import ResultSerializer, ResultExamListSerializer, ResultUserListSerializer
from .permissions import HasCreateAccess, HasUpdateDeleteAccess, HasReadAccess, HasResultsStudentAccess, HasResultsExamAccess
from .utility.query import get_users, get_exams


class ResultViewSet(ModelViewSet):
    queryset = Result.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ResultSerializer
    parser_classes = [FormParser, MultiPartParser]
    http_method_names = ['get', 'delete', 'patch', 'post']

    def get_permissions(self):
        if self.action == "create":
            permission = (IsAuthenticated(), HasCreateAccess(), )

        elif self.action == "partial_update" or self.action == "destroy":
            permission = (IsAuthenticated(), HasUpdateDeleteAccess() )

        elif self.action == "retrieve":
            permission = (IsAuthenticated(), HasReadAccess() )

        else:
            permission = (IsAuthenticated(), )

        return permission



class ResultExamList(ListAPIView):
    serializer_class = ResultExamListSerializer
    permission_classes = (IsAuthenticated, HasResultsExamAccess(), )

    def list(self, request, *args, **kwargs):
        if not is_exist(kwargs['exam_id']):
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            exam = Exam.objects.get(pk=kwargs['exam_id'])
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        users = get_users(exam.id)
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(users, request)
        users_ser = ResultExamListSerializer(result_page, many=True, exam_id=exam.id)
        return paginator.get_paginated_response(users_ser.data)

           

class ResultStudentList(ListAPIView):
    serializer_class = ResultUserListSerializer
    permission_classes = (IsAuthenticated, HasResultsStudentAccess(), )

    def list(self, request, *args, **kwargs):
        if not is_exist(kwargs['student_id']):
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(pk=kwargs['stusent_id'])
            if usre.role != "STUDENT":
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        exams = get_exams(user.id)
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(exams, request)
        exam_ser = ResultUserListSerializer(
            result_page, many=True, student_id=user.id)
        return paginator.get_paginated_response(exam_ser.data)


