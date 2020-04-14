# -*-coding:utf-8
# 封装rpc请求函数
from Log import log
from TypesEnum import *


@log
def SayHelloImplement(ip, data):
    d = dict()
    d['operation'] = DBOperation.Failure
    return d