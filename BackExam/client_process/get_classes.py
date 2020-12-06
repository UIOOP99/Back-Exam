import grpc
from grpc_pb2s import class_pb2, class_pb2_grpc

def get_classes(id):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = class_pb2_grpc.ClassControllerStub(channel)
        user_id = class_pb2.ClassListRequest(id)
        classes = stub.List(user_id)
        return classes

def get_commen_classes(id):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = class_pb2_grpc.ClassControllerStub(channel)
        class_id = class_pb2.ClassCommenRequest(id)
        classes = stub.GetCommenClasses(class_id)
        return classes

        