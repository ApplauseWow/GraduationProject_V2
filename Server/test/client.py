# -*-coding:utf-8-*-
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('localhost:44967')
    # 调用 rpc 服务
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name=bytes('czl')))
    print("Greeter client received: " + response.message, type(response.message))
    response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name=bytes('daydaygo')))
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    run()