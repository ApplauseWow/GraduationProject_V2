# -*-coding:utf-8
# 封装rpc请求函数
from Log import log
from TypesEnum import *
from DBC import DBC


class CallMethodImplement(object):

    __operation_mapper = {
        DBOperation.Failure: ClientRequest.Failure,
        ProcessOperation.Failure: ClientRequest.Failure,
        DBOperation.Success: ClientRequest.Success,
        ProcessOperation.Success: ClientRequest.Success
    }

    __obj2table_mapper = {  # 对象映射到表
        'note': 'note_info',  # 公告
        'user': 'user_info'  # 用户
        # ...
    }

    @log
    def SayHello(self, ip, data):
        """
        用于测试
        :param ip: 用于识别客户端
        :param data:　请求参数
        :return:
        """
        d = dict()
        d['operation'] = ClientRequest.Failure
        d['exception'] = Exception('fail to ...')
        return d

    @log
    def GetRecordsCount(self, ip, data):
        """
        获取总记录条数
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            res = conn.count_record(self.__obj2table_mapper[data['obj']], data['type'])  # _type中是字典与sql_mapper中名称必须一致
            res['operation'] = self.__operation_mapper[res['operation']]
            return res
        except Exception as e:
            return {'operation':ClientRequest.Failure, 'exception':e, 'result': None}

    @log
    def GetAllObjects(self, ip, data):
        """
        获取所有对象
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            table = self.__obj2table_mapper[data['obj']]
            start_end = (data['start'], data['num']) if data['num'] else()
            data.pop('start')
            data.pop('num')
            data.pop('obj')
            res = conn.search_record(table=table, start_end=start_end, limitation=None if data == {} else data)
            res['operation'] = self.__operation_mapper[res['operation']]
            return res
        except Exception as e:
            return {'operation':ClientRequest.Failure, 'exception':e, 'result': None}

    @log
    def VoidTheNote(self, ip, data):
        """
        作废一则公告
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            data['void'] = NoteStatus.Invalid.value
            res = conn.modify_record('void', 'note_info', data)
            res['operation'] = self.__operation_mapper[res['operation']]
            return res
        except Exception as e:
            return {'operation':ClientRequest.Failure, 'exception':e, 'result': None}

    @log
    def InsertAObject(self ,ip, data):
        """
        添加一则新对象
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            table = self.__obj2table_mapper[data['obj']]
            data.pop('obj')
            res = conn.modify_record('insert', table, data)
            res['operation'] = self.__operation_mapper[res['operation']]
            return res
        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def ModifyTheObject(self, ip, data):
        """
        修改对象
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            table = self.__obj2table_mapper[data['obj']]
            data.pop('obj')
            res = conn.modify_record('update', table, data)
            res['operation'] = self.__operation_mapper[res['operation']]
            return res
        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def DeleteTheObject(self, ip, data):
        """
        修改对象
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            table = self.__obj2table_mapper[data['obj']]
            data.pop('obj')
            res = conn.modify_record('delete', table, data)
            res['operation'] = self.__operation_mapper[res['operation']]
            return res
        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def GetTheObject(self, ip, data):
        """
        修改对象
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            table = self.__obj2table_mapper[data['obj']]
            data.pop('obj')
            res = conn.search_record(table=table, start_end=(), limitation=data)
            res['operation'] = self.__operation_mapper[res['operation']]
            return res
        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}