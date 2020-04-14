# -*-coding:utf-8-*-
# 字段位置一一对应

Index2ColName = {  # 按照表(对象)分类
    
    'note': {
        0:'note_id', 1:'title', 2:'detail', 3:'pub_date', 4:'is_valid'
    },

    'user': {
        0:'user_id', 1:'major', 2:'grade', 3:'_class', 4:'user_type', 5:'tel', 6:'email'
    }

    
}

ColName2Index = {  # 按照表(对象)分类

    'note': {v : k for k, v in Index2ColName['note'].items()},

    'user': {v : k for k, v in Index2ColName['user'].items()}

}

'''
select GROUP_CONCAT(COLUMN_NAME) from information_schema.COLUMNS where table_name = 'user_info';
查询字段名称
'''