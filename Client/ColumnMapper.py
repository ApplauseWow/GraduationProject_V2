# -*-coding:utf-8-*-
# 字段位置一一对应

Index2ColName = {  # 按照表(对象)分类
    
    'note': {
        0: 'note_id', 1: 'title', 2: 'detail', 3: 'pub_date', 4: 'is_valid'
    },

    'user': {
        0: 'user_id', 1: 'user_name', 2: 'major', 3: 'grade', 4: '_class', 5: 'user_type', 6: 'tel', 7: 'email'
    }

    
}

ColName2Index = {  # 按照表(对象)分类

    'note': {v: k for k, v in Index2ColName['note'].items()},

    'user': {v: k for k, v in Index2ColName['user'].items()}

}

'''
select GROUP_CONCAT(COLUMN_NAME) from information_schema.COLUMNS where table_name = 'user_info';
查询字段名称
'''