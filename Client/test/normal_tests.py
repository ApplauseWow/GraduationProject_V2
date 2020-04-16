# -*-coding:utf-8-*-
# 用于各种小测试
import sys

from PyQt5.QtWidgets import QApplication

from TypesEnum import *


if __name__ == '__main__':
    from PyQt5.QtWebKitWidgets import QWebView
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QDialog, QGridLayout

    # with open('../ui_design/js/aweek_every_hour_clockIn.js', 'r') as f:
    #     js = f.read()
    # with open('../ui_design/js/html_model.html', 'r') as f:
    #     html = f.read()
    # chart = "".join([html.format(300, 300),
    #                  # "<script type='text/javascript' src='echarts-liquidfill.js'></script>",
    #                  "<script>",
    #                  "var data = {};".format([[0, 1, 5], [5, 3, 9]]),
    #                  # "var clock_in = {};".format(30),
    #                  # "var total = {};".format(50),
    #                  "</script>",
    #                  "<script>",
    #                  js,
    #                  "</script></body></html>"])
    # with open('html.html', 'w') as f:
    #     f.write(chart)

    # import time
    # import datetime
    # start = datetime.datetime.now()
    # print(start, type(start))
    # end = datetime.datetime(2020, 4, 16, 16, 00, 05, 582000)
    # print(end, type(end))
    # sub = end - start
    # print(sub, sub.seconds, float(sub.seconds)/3600, "{:.2f}".format(float(sub.seconds)/3600))

    import os

    # kwargs = dict(
    #     name='柱形图',
    #     x_axis=['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
    #     y_axis=[5, 20, 36, 10, 75, 90]
    #     # bar_category_gap = 0 间距
    # )
    # bar.add(**kwargs)
    # bar.render()

    # app = QApplication(sys.argv)
    # lay = QGridLayout()
    # w = QDialog()
    # win_ = QWebView()
    # p = 'file:///' + os.path.join(os.getcwd(), 'html.html').replace("\\", "/")
    # win_.load(QtCore.QUrl(p))
    # win_.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 影藏窗口
    # win_.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)  # 取消滚动条
    # win_.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
    # win_.resize(300, 400)
    # win_2 = QWebView()
    # win_2.load(QtCore.QUrl('http://www.baidu.com'))
    # win_2.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 影藏窗口
    # win_2.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)  # 取消滚动条
    # win_2.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
    # win_2.resize(300, 400)
    # lay.addWidget(win_, 0, 0, 5, 5)
    # lay.addWidget(win_2, 0, 5, 5, 5)
    # w.setLayout(lay)
    # w.show()
    # win_.show()
    # sys.exit(app.exec_())

    # from cv2.cv2 import imread
    # import dlib
    # from face_recognition import face_locations, face_encodings
    #
    # detector = dlib.get_frontal_face_detector()
    # img = imread('1.jpg')
    # dets = detector(img, 1)
    # print(dets, len(dets))
    # face_location = face_locations(img, model='cnn')
    # _face_location = [].append(face_location[0])
    # print dlib.DLIB_USE_CUDA
    # face_encoding = face_encodings(img, _face_location)  # or here !
    # print(_face_location, face_encoding)

    '''
    sql:
    查询一天：

select * from 表名 where to_days(时间字段名) = to_days(now());

select * from 表名 where date(时间字段名) = curdate();

昨天

select * from 表名 where to_days( now( ) ) - to_days( 时间字段名) <= 1;

7天

select * from 表名 where date_sub(curdate(), interval 7 day) <= date(时间字段名);

一周内数据

select * from 表名 where 时间字段名 between current_date()-7 and sysdate();

近30天

select * from 表名 where date_sub(curdate(), interval 30 day) <= date(时间字段名);

select * from tbl_name where to_days(now()) - to_days(date_col) <= 30; 

本月

select * from 表名 where date_format( 时间字段名, '%Y%m' ) = date_format(curdate( ) , '%Y%m' )


查询一个月

select * from table where date_sub(curdate(), interval 1 month) <= date(column_time);

上一月

select * from 表名 where period_diff( date_format( now( ) , '%Y%m' ) , date_format( 时间字段名, '%Y%m' ) ) =1

 其他时间函数：

(1) select dayofweek(’1998-02-03’);  -> 3      

 dayofweek(date) 返回 date 的星期索引(1 = Sunday, 2 = Monday, ... 7 = Saturday)。索引值符合 ODBC 的标准。 

(2) select weekday(’1998-02-03 22:23:00’); -> 1 

weekday(date) 返回 date 的星期索引(0 = Monday, 1 = Tuesday, ... 6 = Sunday)

(3) select dayofmonth(’1998-02-03’); -> 3

dayofmonth(date) 返回 date 是一月中的第几天，范围为 1 到 31

(4) select dayofyear(’1998-02-03’); -> 34

dayofyear(date) 返回 date 是一年中的第几天，范围为 1 到 366

(5) select month(’1998-02-03’);  -> 2

month(date) 返回 date 中的月份，范围为 1 到 12： 

(6) select dayname("1998-02-05");  -> ’Thursday’

dayname(date) 返回 date 的星期名： 

(7) select monthname("1998-02-05");  -> ’February’

monthname(date) 返回 date 的月份名： 

(8) select quarter(’98-04-01’); -> 2

quarter(date) 返回 date 在一年中的季度，范围为 1 到 4： 

(9) week(date) 

week(date,first) 
对 于星期日是一周中的第一天的场合，如果函数只有一个参数调用，返回 date 为一年的第几周，返回值范围为 0 到 53 (是的，可能有第 53 周的开始)。两个参数形式的 WEEK() 允许你指定一周是否以星期日或星期一开始，以及返回值为 0-53 还是 1-52。 这里的一个表显示第二个参数是如何工作的：

值 含义 
0 一周以星期日开始，返回值范围为 0-53 
1 一周以星期一开始，返回值范围为 0-53 
2 一周以星期日开始，返回值范围为 1-53 
3 一周以星期一开始，返回值范围为 1-53 (ISO 8601)


mysql> select week(’1998-02-20’); 
-> 7 
mysql> select week(’1998-02-20’,0); 
-> 7 
mysql> select week(’1998-02-20’,1); 
-> 8 
mysql> select week(’1998-12-31’,1); 
-> 53

注意，在版本 4.0 中，WEEK(#,0) 被更改为匹配 USA 历法。 注意，如果一周是上一年的最后一周，当你没有使用 2 或 3 做为可选参数时，MySQL 将返回 0： 
mysql> select year(’2000-01-01’), week(’2000-01-01’,0); 
-> 2000, 0 
mysql> select week(’2000-01-01’,2); 
-> 52

你 可能会争辩说，当给定的日期值实际上是 1999 年的第 52 周的一部分时，MySQL 对 week() 函数应该返回 52。我们决定返回 0 ，是因为我们希望该函数返回“在指定年份中是第几周”。当与其它的提取日期值中的月日值的函数结合使用时，这使得 week() 函数的用法可靠。 如果你更希望能得到恰当的年-周值，那么你应该使用参数 2 或 3 做为可选参数，或者使用函数 YEARWEEK() ： 
mysql> select yearweek(’2000-01-01’); 
-> 199952 
mysql> select mid(yearweek(’2000-01-01’),5,2); 
-> 52

year(date) 
返回 date 的年份，范围为 1000 到 9999： 
mysql> select year(’98-02-03’); 
-> 1998

yearweek(date) 
yearweek(date,first) 
返回一个日期值是的哪一年的哪一周。第二个参数的形式与作用完全与 WEEK() 的第二个参数一致。注意，对于给定的日期参数是一年的第一周或最后一周的，返回的年份值可能与日期参数给出的年份不一致： 
mysql> select yearweek(’1987-01-01’); 
-> 198653

注意，对于可选参数 0 或 1，周值的返回值不同于 WEEK() 函数所返回值(0)， WEEK() 根据给定的年语境返回周值。 
hour(time) 
返回 time 的小时值，范围为 0 到 23： 
mysql> select hour(’10:05:03’); 
-> 10

minute(time) 
返回 time 的分钟值，范围为 0 到 59： 
mysql> select minute(’98-02-03 10:05:03’); 
-> 5

second(time) 
返回 time 的秒值，范围为 0 到 59： 
mysql> select SECOND(’10:05:03’); 
-> 3

preiod_add(P,N) 
增加 N 个月到时期 P(格式为 YYMM 或 YYYYMM)中。以 YYYYMM 格式返回值。 注意，期间参数 P 不是 一个日期值： 
mysql> select preiod_add(9801,2); 
-> 199803

period_diff(P1,P2) 
返回时期 P1 和 P2 之间的月数。P1 和 P2 应该以 YYMM 或 YYYYMM 指定。 注意，时期参数 P1 和 P2 不是 日期值： 
mysql> select period_diff(9802,199703); 
-> 11

date_add(date,interval expr type) 
date_sub(date,interval expr type) 
adddate(date,interval expr type) 
subdate(date,interval expr type) 
这 些函数执行日期的算术运算。ADDDATE() 和 SUBDATE() 分别是 DATE_ADD() 和 date_sub() 的同义词。 在 MySQL 3.23 中，如果表达式的右边是一个日期值或一个日期时间型字段，你可以使用 + 和 - 代替 DATE_ADD() 和 date_sub()(示例如下)。 参数 date 是一个 DATETIME 或 DATE 值，指定一个日期的开始。expr 是一个表达式，指定从开始日期上增加还是减去间隔值。expr 是一个字符串；它可以以一个 “-” 领头表示一个负的间隔值。type 是一个关键词，它标志着表达式以何格式被解释。

    '''

    '''
    sql2:
    eg：现有mytable表格中字段dt为datetime格式、mydata为float格式，需要分别按日、月、年查询dt字段内容并求和

1.按日查询：

SELECT sum(mydata) FROM mytable WHERE date(dt)=str_to_date('2012-11-05', '%Y-%m-%d')
 

2.按月查询

SELECT sum(mydata) FROM mytable WHERE month(dt)= month(str_to_date('2012-11-05','%Y-%m-%d'))
——可能这个办法比较麻烦，但是可以执行

3.按年查询

同上

SELECT sum(mydata) FROM mytable WHERE year(dt)= year(str_to_date('2012-11-05','%Y-%m-%d'))
    '''

    """
    筛选:
    时间间隔计算：
    SELECT round(TimeStampDiff(*MINUTE/HOUR/SECOND/WEEK/YEAR/MONTH,*date/datetime,*date/datetime)/60, *精确到小数后几位);
    教师：（所有人）
    今日出勤人数：SELECT count(*) FROM attendance_record WHERE date(date_time)=str_to_date(current_date(), '%Y-%m-%d') and record_type = 0;
    本周每天每个时间段的出勤/离岗人数:但是没有的时间段就没有,但无所谓echarts表格是坐标
    select weekday(date_time), date_format(date_time,'%H'), count(*)
    from attendance_record
    where record_type = 0/1 and date_time between current_date()-weekday(current_date()) and current_date() + 7 - weekday(current_date())
    group by weekday(date_time), date_format(date_time,'%H')
    ORDER BY date_time asc
    
    学生：
    本周每天工作时长：在python中处理更方便，查询后filter按照0-6 Mon-Sun 过滤 再做时差计算感觉用得上reduce函数，跳过不成对数据 eg：0 0 1 则计算第二个0与1 | 0 1 0 不计算最后一个0 | 0 1 1 第二个1跳过其实必须为0 | 1 1 0 跳过前两个1
    (day, record_type, date_time)  date_time - date_time .hour
    select weekday(date_time) as day, record_type, date_time
    from attendance_record
    where user_id = 201610414206 and date_time between current_date()-weekday(current_date()) and current_date() + 7 - weekday(current_date())
    ORDER BY date_time asc;
    本周上岗/离岗时间戳分布：[[星期,小时,坐标图形大小], ]
    select weekday(date_time), date_format(date_time,'%H'), 5
    from attendance_record
    where user_id = 201610414206 and record_type = 0/1 and date_time between current_date()-weekday(current_date()) and current_date() + 7 - weekday(current_date())
    ORDER BY date_time asc
    """