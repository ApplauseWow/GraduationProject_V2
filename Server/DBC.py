# -*-coding:utf-8-*-
import pymysql
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from TypesEnum import *


class DBC(object):
    """
    数据库交互
    """

    client_mapper = "./ClientDBMapper.xml"
    sql_mapper = "./SQLMapper.xml"

    def __init__(self, client_ip):
        tree = ET.parse(self.client_mapper)  # 解析数据库信息xml
        root = tree.getroot()  # 获取根节点
        client_info = dict()  # 客户端映射信息
        res = filter(lambda x: x.get('c_ip') == client_ip, root.findall('client'))  # 查找对应客户端信息
        if not res:  # 未查到对应的客户端信息
            raise Exception("No such a client information!")
        else:  # 已查到
            for pair in res[0].items():
                client_info[pair[0]] = pair[1]
        try:
            self.conn = pymysql.connect(host=client_info['host'],
                                        user=client_info['user'],
                                        db=client_info['db'],
                                        port=int(client_info['port']),
                                        password=client_info['pwd'],
                                        charset='utf8',
                                        connect_timeout = 5
                                        )
        except Exception as e:
            raise Exception("fail to connect to the DB for " + str(e))

    def close_connect(self):
        """
        关闭数据库连接
        :return:None
        """

        if self.conn:
            self.conn.close()
        else:
            pass

    # 一般获取总记录条数
    def count_record(self, table, _type):
        """
        获取总记录的条数
        :param table: 表名
        :param _type: 限制要求　一个字典
        :return: dict{'operation':DBOpertion., 'exception': e, 'result':results | None}
        """

        if _type:  # 有筛选要求
            tree = ET.parse(self.sql_mapper)
            root = tree.getroot()
            res = filter(lambda x: x.get('name') == table, root.findall('table'))  # 找到table的sql
            sql = res[0].find('limited_count').text
        else:  # 没有要求
            sql = "select count(*) from %s" % (table)
        cursor = self.conn.cursor()
        try:
            if _type:
                cursor.execute(sql, _type)
            else:
                cursor.execute(sql)
            results = cursor.fetchone()[0]
            return {'operation': DBOperation.Success, 'exception': None, 'result': results}
        except Exception as e:
            return {'operation': DBOperation.Failure, 'exception': e, 'result': None}
        finally:
            cursor.close()

    # 一般查询操作
    def search_record(self, table, start_end=(), limitation=None):
        """
        获取表所有信息
        :param table:　表名
        :param start_end:　(起始索引号, 一页总条数) | ()
        :return:dict{'operation':DBOpertion., 'exception': e, 'result':results | None}
        """

        if start_end == () and not limitation:  # 不需要分页, 也没有限制
            sql = "select * from %s;" % table
        elif start_end != () and not limitation:  # 需要分页，但没有限制
            sql = "select * from %s limit %s, %s;" % (table, start_end[0], start_end[1])
        elif start_end != () and limitation: # 需要分页且有限制条件
            tree = ET.parse(self.sql_mapper)
            root = tree.getroot()
            res = filter(lambda x: x.get('name') == table, root.findall('table'))  # 找到table的sql
            sql = res[0].find('limited_search').text
            limitation['start'] = start_end[0]
            limitation['num'] = start_end[1]
        elif start_end == () and limitation:  # 不需要分页，但有限制要求
            tree = ET.parse(self.sql_mapper)
            root = tree.getroot()
            res = filter(lambda x: x.get('name') == table, root.findall('table'))  # 找到table的sql
            basic_sql = res[0].find('limited_search').text
            sql = basic_sql[:basic_sql.find('limit')] + ';'
        else:  # 仅仅为代码完整，以上已经枚举所有情况
            sql = ""
        cursor = self.conn.cursor()
        try:
            if not limitation:
                cursor.execute(sql)
            elif limitation:
                cursor.execute(sql, limitation)
            results = cursor.fetchall()
            return {'operation': DBOperation.Success, 'exception': None, 'result': results}
        except Exception as e:
            return {'operation': DBOperation.Failure, 'exception': e, 'result': None}
        finally:
            cursor.close()

    # 一般增删改操作
    def modify_record(self, op, table, para_dict=None):
        """
        添加新记录
        :param op: 操作->insert | delete | update
        :param table: 表名
        :param para_dict: 数据字典
        :return:dict{'operation':DBOpertion., 'exception': e, 'result':None}
        """

        tree = ET.parse(self.sql_mapper)
        root = tree.getroot()
        res = filter(lambda x: x.get('name') == table, root.findall('table'))  # 找到table的sql
        sql = res[0].find(op).text
        cursor = self.conn.cursor()
        try:
            row = cursor.execute(sql,para_dict)
            if row == 1:  # 操作成功
                self.conn.commit()  # 必须提交事务才能生效
                return {'operation': DBOperation.Success, 'exception': None, 'result': None}
            else:  # 操作失败
                return {'operation': DBOperation.Failure, 'exception': Exception("fail to {}".format(op)), 'result': None}
        except Exception as e:  # 操作失败
            return {'operation': DBOperation.Failure, 'exception': e, 'result': None}
        finally:
            cursor.close()


if __name__ == '__main__':
    try:
        db = DBC('127.0.0.1')
        # a = db.get_all_info("user_info", (0, 3))
        # print len(a)
        # print(a == ())
        # for i in a:
        #     print(i)
        # d= dict()
        # d['user_id'] = 1
        # d['grade'] = 1
        # d['_class'] = 1
        # d['email'] = '1'
        # d['tel'] = '1'
        # d['user_type'] = 1
        # b = db.modify_record('insert', 'user_info', d)
        # print(b)
        # from datetime import date
        # a = db.modify_record('insert', 'note_info', {'title':"第二", 'detail': "通知", 'pub_date':date(2020, 10, 1), 'is_valid':1})
        # res = db.search_record('note_info')['result']
        # print(res[2][1], type(res[2][1]), res[2][1], type(res[2][1]))
        # print(u"{}".format(res[2][4]))
        # print db.count_record('note_info', {'is_valid': 1})['result']
        # a = "SELECT * FROM `note_info` WHERE `is_valid`=%(is_valid)s limit %(start)s, %(num)s;"
        # index = a.find('limit')
        # s = a[:index]+';'
        # print(s)
        # print db.search_record('user_info', (0, 8))['result']
        # print str(None)=='None'
        print db.search_record('user_info', (), {'user_id': 2})['result']

    except Exception as e:
        print(e)



