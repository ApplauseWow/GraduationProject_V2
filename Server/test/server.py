# -*-coding:utf-8-*-
from concurrent import futures
import time
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import pickle
from CallMethodImplement import *

# 实现 proto 文件中定义的 GreeterServicer
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    # 实现 proto 文件中定义的 rpc 调用
    def SayHello(self, request, context):
        ip = str(context.peer()).split(':')[1]
        data = {'name':request.name, 'a':1, 'b':[1,2]}
        res = SayHelloImplement(ip=ip, data=data)
        return helloworld_pb2.HelloReply(message = pickle.dumps(res))

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message= pickle.dumps('hello {msg}'.format(msg = context.peer())))

def serve():
    # 启动 rpc 服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:5005')
    server.start()
    try:
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()