from .models import User
from django_grpc_framework import generics
from account.serializers import UserProtoSerializer


class UserService(generics.ModelService):
    queryset = User.objects.all()
    serializer_class = UserProtoSerializer