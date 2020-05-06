# -*-coding:utf-8
# 封装rpc请求函数
import re

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
        'user': 'user_info',  # 用户
        'attendance': 'attendance_record'  # 考勤记录
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
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

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
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

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
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def InsertAObject(self, ip, data):
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
        修改一个对象
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
        删除一个对象
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
        获取一个对象
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

    @log
    def GetClockInOrOutTimeStamp(self, ip, data):
        """
        获取上岗/离岗时间戳
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            table = self.__obj2table_mapper[data['obj']]
            data.pop('obj')
            data['record_type'] = AttendanceType.ClockIn.value
            res_clock_in = conn.special_search(table=table, op='self_timestamp_search', data=data)
            data['record_type'] = AttendanceType.ClockOut.value
            res_clock_out = conn.special_search(table=table, op='self_timestamp_search', data=data)
            if res_clock_in['operation'] == DBOperation.Failure or res_clock_out['operation'] == DBOperation.Failure:  # 其一操作失败
                res = {'operation': ClientRequest.Failure, 'exception': Exception('fail to get the clock in/out timestamp'), 'result': None}
            else:  # 双双成功
                hour_mapper = {'00': 0, '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6,
                               '07': 7, '08': 8, '09': 9, '10': 10, '11': 11,
                               '12': 12, '13': 13, '14': 14, '15': 15, '16': 16, '17': 17,
                               '18': 18, '19': 19, '20': 20, '21': 21, '22': 22, '23': 23}
                clock_in = res_clock_in['result']
                clock_out = res_clock_out['result']
                clock_in_list = map(lambda x: [x[0], hour_mapper[x[1]], x[2]], clock_in)
                clock_out_list = map(lambda x: [x[0], hour_mapper[x[1]], x[2]], clock_out)
                res = {'operation': ClientRequest.Success, 'exception': None, 'result': {'clock_in': clock_in_list, 'clock_out': clock_out_list}}
            return res
        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def GetWorkHourEverYDay(self, ip, data):
        """
        获取本周工作时长
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            table = self.__obj2table_mapper[data['obj']]
            data.pop('obj')
            res = conn.special_search(table=table, op='self_week_search', data=data)
            res['operation'] = self.__operation_mapper[res['operation']]
            if res['operation'] == ClientRequest.Failure:  # 失败
                return res
            else:  # 成功，处理数据
                # 计算本周每日在岗时长
                week_hours = []
                for day in range(7):
                    today_records = filter(lambda record: record[0] == day, res['result'])  # 今日打卡记录
                    record_type_sequence = "".join([str(record[1]) for record in today_records])  # 打卡记录类型序列，用于检测并定位有效计算对
                    # 扫描序列，定位有效对
                    pattern = re.compile(r"01")
                    location = [match_obj.span()[0] for match_obj in re.finditer(pattern, record_type_sequence)]
                    # 计算时差
                    hours = map(lambda index: (today_records[index + 1][2] - today_records[index][2]).seconds, location)
                    # 雷家时长
                    today_hours = float(reduce(lambda a, b: a + b, hours, 0))/3600
                    # 星期day加入本周时长列表
                    week_hours.append(round(today_hours, 3))
                res['result'] = week_hours
                return res
        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def GetClockInOrOutCountEachHour(self, ip, data):
        """
        获取本周每日每个时刻上岗和离岗人数
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            res_clock_in = conn.special_search(self.__obj2table_mapper[data['obj']], 'all_each_time_count', {'record_type': AttendanceType.ClockIn.value})
            res_clock_out = conn.special_search(self.__obj2table_mapper[data['obj']], 'all_each_time_count', {'record_type': AttendanceType.ClockIn.value})
            if res_clock_in['operation'] == DBOperation.Failure or res_clock_out['operation'] == DBOperation.Failure:  # 其一操作失败
                res = {'operation': ClientRequest.Failure, 'exception': Exception('fail to get the clock in and out count each hour'), 'result': None}
            else:  # 双双成功
                hour_mapper = {'00': 0, '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6,
                               '07': 7, '08': 8, '09': 9, '10': 10, '11': 11,
                               '12': 12, '13': 13, '14': 14, '15': 15, '16': 16, '17': 17,
                               '18': 18, '19': 19, '20': 20, '21': 21, '22': 22, '23': 23}
                clock_in = res_clock_in['result']
                clock_out = res_clock_out['result']
                clock_in_list = map(lambda x: [x[0], hour_mapper[x[1]], x[2]], clock_in)
                clock_out_list = map(lambda x: [x[0], hour_mapper[x[1]], x[2]], clock_out)
                res = {'operation': ClientRequest.Success, 'exception': None, 'result': {'clock_in': clock_in_list, 'clock_out': clock_out_list}}
            return res
        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def GetClockInRateToday(self, ip, data):
        """
        获取今日上岗人数和工作室总人数以计算出勤率
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:
            conn = DBC(client_ip=ip)
            res_today = conn.special_search(self.__obj2table_mapper[data['obj']], 'today_clockin_count')  # _type中是字典与sql_mapper中名称必须一致
            res_total = conn.count_record(self.__obj2table_mapper['user'], {'user_type': UserType.Student.value})
            if res_today['operation'] == DBOperation.Failure or res_total['operation'] == DBOperation.Failure:
                res = {'operation': ClientRequest.Failure, 'exception': Exception('fail to get the clock in rate today'), 'result': None}
            else:
                clock_in = res_today['result'][0][0]
                total = res_total['result']
                res = {'operation': ClientRequest.Success, 'exception': None, 'result': {'clock_in': clock_in, 'total': total}}
            return res
        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def CheckIdentityByFace(self, ip, data):
        """
        通过人脸匹配用户信息
        :param ip: 用于识别客户端
        :param data: 请求参数
        :return: dict{'operation': , 'exception': , 'result': }
        """

        try:

        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}

    @log
    def Register(self, ip, data):
        try:

        except Exception as e:
            return {'operation': ClientRequest.Failure, 'exception': e, 'result': None}


# test
if __name__ == '__main__':
    print(CallMethodImplement().GetClockInRateToday(ip='127.0.0.1', data={'obj': 'attendance'}))