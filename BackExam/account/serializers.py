from .models import User
from django_grpc_framework import proto_serializers
from grpc_pb2s import user_pb2


class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = User
        proto_class = user_pb2.User
        fields = ['id', 'role']