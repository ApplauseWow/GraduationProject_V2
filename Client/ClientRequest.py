# -*-coding:utf-8-*-
# rpc协议除基本数据类型以外的其他类型需要利用pickle模块序列化为字节流形式pickle.dump来传输
from rpc_protocol import correspondence_pb2, correspondence_pb2_grpc
import grpc
from TypesEnum import *
try:
    import cPickle as pickle
except:
    import pickle


class CR(object):
    """
    客户端请求连接
    """

    _HOST = '127.0.0.1'  # 192.168.
    _PORT = '44967'

    def __init__(self):
        self.channel = grpc.insecure_channel("{server}:{port}".format(server=self._HOST, port=self._PORT))
        self.stub = correspondence_pb2_grpc.BackendStub(self.channel)
        try:
            grpc.channel_ready_future(self.channel).result(timeout=1)
        except Exception as e:
            print(e)
            self.channel.close()
            raise Exception("连接失败")

    def CloseChannel(self):
        self.channel.close()

    def SayHelloRequest(self):
        """
        用于测试
        :return:
        """

        response = self.stub.SayHello(correspondence_pb2.HelloRequest(para=pickle.dumps('test')))
        print(pickle.loads(response.result), type(response.result))

    # 共用
    def GetCountRequest(self,obj,  _type=None):
        """
        获取总记录条数
        :param obj: 对象 eg: 'note', 'project' 'user' ...
        :param _type: 是否有分类 eg: NoteStatus.Valid.value | ... 可能是一组{用字典对应}
        :return: res['result'] -> 条数
        """

        try:
            data = {'obj': obj, 'type': _type}
            response = self.stub.GetRecordsCount(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:  # 请求失败
                raise Exception('fail to get count!')
            elif res['operation'] == ClientRequest.Success:  # 请求成功
                return res['result']
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    # 公告相关
    def GetAllNotesRequest(self, start=None, num=None, is_valid=None):
        """
        获取所有公告
        :param start:　限制田间，起始位置
        :param num:　限制条件，每页条数
        :param is_valid: 限制条件，公告过期|未过期
        :return:(...)
        """

        try:
            data = {'obj': 'note', 'start': start, 'num': num, 'is_valid': is_valid}
            response = self.stub.GetAllNotes(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:  # 请求失败
                return ()
            elif res['operation'] == ClientRequest.Success:  # 请求成功
                return res['result']
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def VoidTheNoteRequest(self, pk):
        """
        作废一则公告
        :param pk:主键　可能是一组　用字典对应
        :return:res['operation'] 即ClientRequest.Sucess | ...
        """

        try:
            data = {'note_id': pk[0]}
            response = self.stub.VoidTheNote(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to void!')
            elif res['operation'] == ClientRequest.Success:
                return ClientRequest.Success
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def InsertANoteRequest(self, data):
        """
        添加一则新公告
        :param data:数据
        :return: res['operation'] 即ClientRequest.Sucess | ...
        """

        try:
            response = self.stub.InsertANote(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to insert!')
            elif res['operation'] == ClientRequest.Success:
                return ClientRequest.Success
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def ModifyTheNoteRequest(self, data):
        """
        修改一则新公告
        :param data:数据
        :return: res['operation'] 即ClientRequest.Sucess | ...
        """

        try:
            response = self.stub.ModifyTheNote(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to modify!')
            elif res['operation'] == ClientRequest.Success:
                return ClientRequest.Success
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    # 用户相关
    def GetAllUserRequest(self, start=None, num=None):
        """
        获取所有公告
        :param start:　限制田间，起始位置
        :param num:　限制条件，每页条数
        :return:
        """

        try:
            data = {'obj': 'user', 'start': start, 'num': num}
            response = self.stub.GetAllUsers(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:  # 请求失败
                return ()
            elif res['operation'] == ClientRequest.Success:  # 请求成功
                return res['result']
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def DeleteTheUserRequest(self, pk):
        """
        删除一个用户
        :param pk:主键　可能是一组　用字典对应
        :return:res['operation'] 即ClientRequest.Sucess | ...
        """

        try:
            data = {'user_id': pk[0]}
            response = self.stub.DeleteTheUser(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to delete!')
            elif res['operation'] == ClientRequest.Success:
                return ClientRequest.Success
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def InsertAUserRequest(self, data):
        """
        添加一个新用户
        :param data:数据
        :return: res['operation'] 即ClientRequest.Success | ...
        """

        try:
            response = self.stub.InsertAUser(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to insert!')
            elif res['operation'] == ClientRequest.Success:
                return ClientRequest.Success
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def ModifyTheUserRequest(self, data):
        """
        修改一则用户信息
        :param data:数据
        :return: res['operation'] 即ClientRequest.Success | ...
        """

        try:
            response = self.stub.ModifyTheUser(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to modify!')
            elif res['operation'] == ClientRequest.Success:
                return ClientRequest.Success
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def GetSelfInfoRequest(self, data):
        """
        获取个人用户信息
        :param data:数据
        :return: res['result'][0] -> {个人信息字典}
        """

        try:
            response = self.stub.GetTheUser(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to modify!')
            elif res['operation'] == ClientRequest.Success:
                return res['result'][0]
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    # 考勤相关
    def GetWorkHourEveryDayRequest(self, data):
        """
        获取本周每日工作时长
        :param data:数据
        :return: res['result'] -> [每日工作时长列表]
        """

        try:
            response = self.stub.GetWorkHourEverYDay(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to get work hour!')
            elif res['operation'] == ClientRequest.Success:
                return res['result']
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def GetClockInOrOutTimeStampRequest(self, data):
        """
        获取本周上岗/离岗时间戳
        :param data:数据
        :return: res['result'] -> [[星期,小时,坐标点大小(定值)]：图表坐标点,...]
        """

        try:
            response = self.stub.GetClockInOrOutTimeStamp(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to get timestamp!')
            elif res['operation'] == ClientRequest.Success:
                return res['result']
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def GetClockInOrOutCountEachHourRequest(self, data):
        """
        获取本周上岗和离岗每个时间段的人数
        :param data:数据->None
        :return: res['result'] -> [[星期,小时,人数]：图表坐标点,...]
        """

        try:
            response = self.stub.GetClockInOrOutCountEachHour(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to get count each hour!')
            elif res['operation'] == ClientRequest.Success:
                return res['result']
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    def GetClockInRateTodayRequest(self, data):
        """
        获取今日到岗人数
        :param data:数据
        :return: res['result'] -> {'clock_in':, 'total': }
        """

        try:
            response = self.stub.GetClockInRateToday(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                raise Exception('fail to get clock in rate!')
            elif res['operation'] == ClientRequest.Success:
                return res['result']
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('fail to request!')

    # 人脸相关
    def CheckIdentityByFaceRequest(self, data):
        """
        通过人脸识别匹配用户信息
        :param data:数据
        :return: res['result'] -> dict{'user_name', 'user_type', 'user_name'}
        """

        try:
            response = self.stub.CheckIdentityByFace(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                return res
            elif res['operation'] == ClientRequest.Success:
                return res
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('请求失败')

    def RegisterRequest(self, data):
        """
        人脸注册
        :param data:数据
        :return: res['result'] -> None
        """

        try:
            response = self.stub.Register(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                return res
            elif res['operation'] == ClientRequest.Success:
                return res
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('请求失败')

    def ClockInOrOutRequest(self, data):
        """
        人脸考勤
        :param data:数据
        :return: {'operation':, 'exception':, 'result':}
        """

        try:
            response = self.stub.ClockInOrOut(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            if res['operation'] == ClientRequest.Failure:
                return res
            elif res['operation'] == ClientRequest.Success:
                return res
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('请求失败')

    # 工位相关
    def GetSeatsDeploymentRequest(self):
        """
        获取工位部署情况(所有工位信息)
        :return:(...)
        """

        try:
            data = {'obj': 'seat'}
            response = self.stub.GetSeatsDeployment(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            return res
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('请求失败')

    def GetSeatsArrangementRequest(self):
        """
        获取工位安排情况(所有工位安排信息)
        :return:(...)
        """

        try:
            data = {'obj': 'seat_arrangement'}
            response = self.stub.GetSeatsArrangement(correspondence_pb2.RequestStruct(para=pickle.dumps(data)))
            res = pickle.loads(response.result)
            return res
        except Exception as e:  # 界面捕捉异常并弹出警告窗口
            print(e)
            raise Exception('请求失败')
