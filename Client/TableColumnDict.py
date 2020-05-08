# -*-coding:utf-8-*-
# 这些数据即使存在外村也依然会全部读取到内存，索性一次性读取还能减少磁盘IO
from TypesEnum import *


def _add_operation(name):
    """
    添加操作列
    :param name: 页面名称
    :return: list
    """

    l = []
    l.extend(__BASIC_COLUMN_DICT[name])
    l.append({'name': u'操作', 'is_hidden': False, 'is_pk': False})
    return l


__BASIC_COLUMN_DICT = {  # 按页面分类的基本字段列表

    'note': [
                {'name': 'id', 'is_hidden': True, 'is_pk': True},
                {'name': u'标题', 'is_hidden': False, 'is_pk': False},
                {'name': u'内容', 'is_hidden': False, 'is_pk': False},
                {'name': u'发布日期', 'is_hidden': False, 'is_pk': False},
                {'name': 'is_valid', 'is_hidden': True, 'is_pk': False},
            ],

    'user': [
                {'name': u'学号|工号', 'is_hidden': False, 'is_pk': True},
                {'name': u'姓名', 'is_hidden': False, 'is_pk': False},
                {'name': u'专业', 'is_hidden': False, 'is_pk': False},
                {'name': u'年级', 'is_hidden': False, 'is_pk': False},
                {'name': u'班', 'is_hidden': False, 'is_pk': False},
                {'name': u'用户类型', 'is_hidden': False, 'is_pk': False, 'convert': lambda x: u"教师" if UserType(x) == UserType.Teacher else u"学生"},
                {'name': u'联系电话', 'is_hidden': False, 'is_pk': False},
                {'name': u'邮箱地址', 'is_hidden': False, 'is_pk': False}
            ],

    'seat_arrangement': [
                {'name': 'arrangement_id', 'is_hidden': True, 'is_pk': True},
                {'name': u'姓名', 'is_hidden': False, 'is_pk': False},
                {'name': u'行', 'is_hidden': False, 'is_pk': False},
                {'name': u'列', 'is_hidden': False, 'is_pk': False},
                {'name': u'负责人', 'is_hidden': False, 'is_pk': False, 'convert': lambda x: u"是" if SeatMember(x) == SeatMember.Leader else u"否"},
                {'name': 'seat_id', 'is_hidden': True, 'is_pk': False},
                {'name': 'user_id', 'is_hidden': True, 'is_pk': False}
            ]

}

TABLE_COLUMN_DICT = {  # 按角色功能分类

    UserType.Teacher: {  # 教师拥有权限

        'current_note': _add_operation('note'),
        'previous_note': __BASIC_COLUMN_DICT['note'],
        'user': _add_operation('user'),
        'seat_arrangement': _add_operation('seat_arrangement')
    },

    UserType.Student: {  # 学生拥有权限

        'current_note': __BASIC_COLUMN_DICT['note'],
        'seat_arrangement': __BASIC_COLUMN_DICT['seat_arrangement']
    }

}
