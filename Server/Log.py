# -*-coding:utf-8-*-
import time
from TypesEnum import *


LOG_PATH = "./client_log"


def log(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if res['operation'] == ClientRequest.Failure:  # 操作失败
            record = "{} : {} at {}, but fail, as {}\n".format(kwargs['ip'], func.__name__, time.asctime(time.localtime(time.time())), res['exception'])
            with open(LOG_PATH, 'a') as f:
                f.write(record)
            return res
        elif res['operation'] == ClientRequest.Success:  # 操作成功
            record = "{} : {} at {}\n".format(kwargs['ip'], func.__name__, time.asctime(time.localtime(time.time())))
            with open(LOG_PATH, 'a') as f:
                f.write(record)
            return res
    return wrapper
