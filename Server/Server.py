# -*-coding:utf-8-*-
import grpc
from rpc_protocol import correspondence_pb2, correspondence_pb2_grpc
from concurrent import futures
import time
from CallMethodImplement import CallMethodImplement
try:
    import cPickle as pickle
except:
    import pickle

_MAX_WORKER = 10
_PERMIT_CLIENTS = 'localhost'  # '[::]'
_PORT = '44967'
_ONE_DAY_IN_SECONDS = 60*60*24


class BackendService(correspondence_pb2_grpc.BackendServicer):

    call_method = CallMethodImplement()

    # 实现proto文件里定义的rpc调用接口
    def SayHello(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        # 业务实现函数
        # func(ip = ip, data = data)
        res = self.call_method.SayHello(ip=ip, data=data)
        return correspondence_pb2.HelloResponse(result=pickle.dumps(res))

    def SayHelloAgain(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        # 业务实现函数
        # func(ip = ip, data = data)
        return correspondence_pb2.HelloResponse(result=pickle.dumps('test'))

    def GetRecordsCount(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        res = self.call_method.GetRecordsCount(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def GetAllNotes(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        res = self.call_method.GetAllObjects(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def InsertANote(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'note'
        res = self.call_method.InsertAObject(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def ModifyTheNote(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'note'
        res = self.call_method.ModifyTheObject(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def VoidTheNote(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        res = self.call_method.VoidTheNote(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def GetAllUsers(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        res = self.call_method.GetAllObjects(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def InsertAUser(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'user'
        res = self.call_method.InsertAObject(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def ModifyTheUser(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'user'
        res = self.call_method.ModifyTheObject(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def DeleteTheUser(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'user'
        res = self.call_method.DeleteTheObject(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def GetTheUser(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'user'
        res = self.call_method.GetTheObject(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def GetClockInOrOutTimeStamp(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'attendance'
        res = self.call_method.GetClockInOrOutTimeStamp(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def GetWorkHourEverYDay(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'attendance'
        res = self.call_method.GetWorkHourEverYDay(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def GetClockInOrOutCountEachHour(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'attendance'
        res = self.call_method.GetClockInOrOutCountEachHour(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def GetClockInRateToday(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        data['obj'] = 'attendance'
        res = self.call_method.GetClockInRateToday(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def CheckIdentityByFace(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        res = self.call_method.CheckIdentityByFace(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))

    def Register(self, request, context):
        ip = str(context.peer()).split(':')[1]  # 客户端ip
        data = pickle.loads(request.para)  # 请求参数
        res = self.call_method.Register(ip=ip, data=data)
        return correspondence_pb2.ResponseStruct(result=pickle.dumps(res))


def service():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_MAX_WORKER))
    correspondence_pb2_grpc.add_BackendServicer_to_server(BackendService(), server)
    server.add_insecure_port("{client}:{port}".format(client=_PERMIT_CLIENTS, port=_PORT))
    server.start()
    # 一直阻塞保持服务状态，当ctrl+C时停止服务
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt as e:
        print("stop the service")
        server.stop(0)


if __name__ == '__main__':
    service()
