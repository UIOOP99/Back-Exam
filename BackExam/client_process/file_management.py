import grpc
from grpc_pb2s import file_pb2, file_pb2_grpc
from BackExam.settings import FILE_SYSTEM_URL

def delete_file(id):
    with grpc.insecure_channel(FILE_SYSTEM_URL) as channel:
        stub = file_pb2_grpc.FileControllerStub(channel)
        file_id = file_pb2.FileId(id=id)
        stub.DestroyFile(file_id)

def create_file(file):
   with grpc.insecure_channel(FILE_SYSTEM_URL) as channel: 
       stub = file_pb2_grpc.FileControllerStub(channel) 
       name = file.name
       data = file.read()
       content = file_pb2.File(content=data, name=name)
       result = stub.CreateFile(content)
       return result.id

def retrieve_file(id):
    with grpc.insecure_channel(FILE_SYSTEM_URL) as channel:  
        stub = file_pb2_grpc.FileControllerStub(channel) 
        file_id = file_pb2.FileId(id=id)
        result = stub.RetrieveFile(file_id)
        return result.url

