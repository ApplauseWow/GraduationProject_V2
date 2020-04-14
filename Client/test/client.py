# -*-coding:utf-8-*-
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import pickle



class CR(object):
    def __init__(self):
        # 连接 rpc 服务器
        self.channel = grpc.insecure_channel('192.168.2.104:5005')
        # 调用 rpc 服务
        self.stub = helloworld_pb2_grpc.GreeterStub(self.channel)

    def SayHelloRequest(self):
        response = self.stub.SayHello(helloworld_pb2.HelloRequest(name=bytes('czl')))
        print("Greeter client received: " + response.message)
        response = self.stub.SayHelloAgain(helloworld_pb2.HelloRequest(name=bytes('daydaygo')))
        print("Greeter client received: " + pickle.loads(response.message))


if __name__ == '__main__':
    CR().SayHelloRequest()