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
from .serializers import ResultSerializer
from .permissions import HasCreateAccess, HasUpdateDeleteAccess, HasReadAccess


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
    
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        pass

class ResultStudent(ListAPIView):

    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        pass


