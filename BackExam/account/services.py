from .models import User
from django_grpc_framework import generics
from account.serializers import UserProtoSerializer


class UserService(generics.CreateService, generics.UpdateService, generics.DestroyService):
    queryset = User.objects.all()
    serializer_class = UserProtoSerializer

    def Update(self, request, context):
        instance = self.get_object()
        serializer = self.get_serializer(instance, message=request, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return serializer.message
