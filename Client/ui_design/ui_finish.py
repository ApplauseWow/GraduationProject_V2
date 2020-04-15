# -*-coding:utf-8-*-
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QDialog, QLabel, QLCDNumber, QGridLayout, QPushButton, \
    QLineEdit, QVBoxLayout, QHBoxLayout, QHeaderView, QMessageBox, QTableWidget, QAbstractItemView, QTableWidgetItem, \
    QFrame, QStackedLayout, QTextEdit, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QEvent, QUrl
import time
import re

from main_win import Ui_MainWindow
from id_info_win import Ui_id_info_win
from warning_win import Ui_warning_win
from register_win import Ui_register_win
from note_detail import Ui_Note_Detail_Win


class DIYLabel(QLabel):
    """
    自定义Label控件
    拥有点击事件响应的Label
    """

    clicked = pyqtSignal()  # 定义信号量

    def mouseReleaseEvent(self, QMouseEvent):
        """
        鼠标松开时触发
        :param QMouseEvent:鼠标事件
        :return: None
        """

        if QMouseEvent.button() == Qt.LeftButton:  # 鼠标左键松开
            self.clicked.emit()  # 发送信号


class MainWindow(Ui_MainWindow, QMainWindow):
    """
    主界面二次设计
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        # 获取桌面尺寸
        desktop = QApplication.desktop()
        desk_width = desktop.screenGeometry().width()
        desk_height = desktop.screenGeometry().height()

        # 摄像头图像设置
        self.frame = DIYLabel(self)
        self.frame.setGeometry(0, 0, desk_width, desk_height)

        self.setupUi(self)

        # 按钮定位
        self.buttons = [self.att_rec, self.face_login, self.face_rec, self.face_reg]
        map(lambda x: x.move(desk_width*0.80, desk_height*0.33+self.buttons.index(x)*(x.height()+8)), self.buttons)
        map(lambda x: x.raise_(), self.buttons)

        # 设置时钟
        self.clock = QLCDNumber(self)
        self.clock.setDigitCount(10)
        self.clock.setMode(QLCDNumber.Dec)
        self.clock.setSegmentStyle(QLCDNumber.Flat)
        self.clock.display(time.strftime("%X", time.localtime()))
        self.clock.setStyleSheet("QLCDNumber{color:rgba(255,0,0,100);}")
        self.clock.resize(280, 120)
        self.clock.move(50, desk_height - 30 - self.clock.height())

        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏窗口
        self.showFullScreen()  # 窗体全屏


class InfoWindow(Ui_id_info_win, QDialog):
    """
    个人信息窗口二次设计
    """

    def __init__(self):
        super(InfoWindow, self).__init__()
        self.setupUi(self)

        # 获取桌面尺寸
        desktop = QApplication.desktop()
        desk_width = desktop.availableGeometry().width()
        desk_height = desktop.availableGeometry().height()

        # 窗体定位
        self.move(int(desk_width*0.3), int(desk_height*0.3))

        # 修改label样式
        labels = [self.l_id, self.l_name, self.l_type, self.user_id, self.user_name, self.user_type]
        map(lambda x: x.setStyleSheet("QLabel{"
                                      "                   background-color:rgba(255,165,0,150);"
                                      "                   border-style:outset;                  "
                                      "                   border-width:4px;                     "
                                      "                   border-radius:10px;                "
                                      "                   border-color:rgba(255,255,255,30);   "
                                      "                   font:bold 18px;                    "
                                      "                   color:rgb(255,255,255);                "
                                      "                   padding:6px; "
                                      "                   text-align: center;                      "
                                      "                   }"),labels)

        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 影藏窗口


class WarningWindow(QDialog, Ui_warning_win):
    """
    识别失败，警告窗口二次设计
    """

    def __init__(self):
        super(WarningWindow, self).__init__()
        self.setupUi(self)

        # 获取桌面尺寸
        desktop = QApplication.desktop()
        desk_width = desktop.availableGeometry().width()
        desk_height = desktop.availableGeometry().height()

        # 窗体定位
        self.move(int(desk_width * 0.3), int(desk_height * 0.3))

        # 设置警告图片和提示语
        self.pix = QPixmap('./ui_design/warning.png').scaled(100, 100)  # 此路径在GUI加载时必须以GUI路径为当前路径，不是此文件
        self.warning.setPixmap(self.pix)
        self.words.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 影藏窗口


class RegisterWindow(QDialog, Ui_register_win):
    """
    人脸注册窗口二次设计
    """

    def __init__(self):
        super(RegisterWindow, self).__init__()
        self.setupUi(self)
        self.input_id.installEventFilter(self)

        # 获取桌面尺寸
        desktop = QApplication.desktop()
        desk_width = desktop.screenGeometry().width()
        desk_height = desktop.screenGeometry().height()

        # 移动窗口
        self.move(int(desk_width*0.3), int(desk_height*0.3))

        # 设置按钮样式
        buttons = [self.bt_again, self.bt_cancel, self.bt_reg]
        map(lambda x: x.setStyleSheet("QPushButton{"
"                   background-color:rgba(255,165,0,80);"
"                   border-style:outset;                  "
"                   border-width:4px;                     "
"                   border-radius:10px;                "
"                   border-color:rgba(255,255,255,80);   "
"                   font:bold 18px;                    "
"                   color:rgba(0,0,0,100);                "
"                   padding:6px;                       "
"                   }"
"                   QPushButton:pressed{"
"                   background-color:rgba(255,165,0,200);"
"                   border-color:rgba(255,255,255,30);"
"                   border-style:inset;"
"                   color:rgba(0,0,0,100);"
"                   }"
"                   QPushButton:hover{"
"                   background-color:rgba(255,165,0,100);"
"                   border-color:rgba(255,255,255,200);"
"                   color:rgba(0,0,0,200);"
"                   }"), buttons)

        # 设置进度条
        self.process.setStyleSheet("QProgressBar "
                                   "{border: 2px solid rgba(255,165,0,255);"
                                   "border-radius: 5px;"
                                   "text-align: center;}"
                                   "QProgressBar::chunk "
                                   "{border: 1px solid rgba(255, 255, 255, 255);"
                                   "border-radius:4px;"
                                   "width: 15px;"
                                   "background:rgba(255,165,0,150);}")
        self.process.setMinimum(0)
        self.process.setMaximum(100)
        self.process.hide()

        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 影藏窗口


class ManagementWindow(QDialog):
    """
    资源管理系统界面
    """

    def __init__(self, user_id, user_type):
        super(ManagementWindow, self).__init__()
        self.user_id = user_id
        self.user_type = user_type
        self.menu_dict = dict()  # 菜单按钮对应的索引号
        # 界面总体布局控件
        self.whole_layout = QGridLayout()
        self.left_menu = QWidget()
        self.left_layout = QGridLayout()
        self.right_page = QWidget()
        self.right_layout = QStackedLayout()  # 右侧主界面采用堆叠布局切换页面
        self.setObjectName("management")
        self.setStyleSheet("#management{background-color: white;}")
        self.right_page.setObjectName("right_page")
        self.right_page.setStyleSheet('''#right_page{border-left:3px solid orange}''')

        # 左侧菜单按钮
        # --公共组
        self.bt_close = QPushButton(u"退出")
        self.bt_close.setObjectName("exit")
        self.bt_note = QPushButton(u"公告管理" if self.user_type == 1 else u"查看公告")
        self.bt_note.setObjectName("note")
        self.bt_group = QPushButton(u"分组管理" if self.user_type == 1 else u"查看分组")
        self.bt_group.setObjectName("group")
        self.bt_source = QPushButton(u"资源管理" if self.user_type == 1 else u"查看资源")
        self.bt_source.setObjectName("source")
        self.bt_attendance = QPushButton(u"考勤统计")
        self.bt_attendance.setObjectName("attendance")
        self.bt_permit = QPushButton(u"假条审批" if self.user_type == 1 else u"假条管理")
        self.bt_permit.setObjectName("permit")
        self.bt_project = QPushButton(u"项目管理" if self.user_type == 1 else u"查看项目")
        self.bt_project.setObjectName("project")
        self.bt_achievement = QPushButton(u"成就管理" if self.user_type == 1 else u"个人成就")
        self.bt_achievement.setObjectName("achievement")
        self.bt_competition = QPushButton(u"比赛管理" if self.user_type == 1 else u"参与比赛")
        self.bt_competition.setObjectName("competition")
        self.bt_task = QPushButton(u"任务分配" if self.user_type == 1 else u"查看任务")
        self.bt_task.setObjectName("task")
        self.bt_seat = QPushButton(u"工位管理" if self.user_type == 1 else u"查看工位")
        self.bt_seat.setObjectName("seat")
        self.bts_pub = [self.bt_note, self.bt_attendance, self.bt_group,
                        self.bt_project,self.bt_competition, self.bt_achievement,
                        self.bt_permit, self.bt_source, self.bt_task,
                        self.bt_seat, self.bt_close]
        # --教师组
        self.bt_t_stuff = QPushButton(u"人事管理")
        self.bt_t_stuff.setObjectName("stuff")
        self.bts_teacher = [self.bt_t_stuff]
        # --学生组
        self.bt_s_selfInfo = QPushButton(u"个人信息")
        self.bt_s_selfInfo.setObjectName("self_info")
        self.bts_stu = [self.bt_s_selfInfo]

        self.init_ui()

    def init_ui(self):
        """
        初始化界面
        :param user_type:用户类型 学生０　教师１
        :return: None
        """

        # 界面布局
        self.left_menu.setLayout(self.left_layout)
        self.right_page.setLayout(self.right_layout)

        # 组合按钮
        self.bts = self.bts_teacher if self.user_type == 1 else self.bts_stu
        self.bts.extend(self.bts_pub)

        # 根据按钮个数设置左右布局
        self.whole_layout.addWidget(self.left_menu, 0, 0, len(self.bts), 2)  # 左部菜单在０行０列开始占１２行３列
        self.whole_layout.addWidget(self.right_page, 0, 2, len(self.bts), len(self.bts)-2)  # 右部页面在０行３列开始占１２行１０列

        # 布置按钮
        for row, bt in enumerate(self.bts):  # 排列按钮
            self.menu_dict[bt.objectName()] = row
            self.left_layout.addWidget(bt, row, 0, 1, 3)  # 从row行0列开始占1行3列
            bt.setStyleSheet("QPushButton{"
"                   background-color:rgba(255,255,255,255);"
"                   border-style:outset;                  "
"                   border-width:2px;                     "
"                   border-radius:20px;                "
"                   border-color:rgba(255,165,0,100);   "
"                   font:bold 23px;                    "
"                   color:rgba(255,165,0,130);                "
"                   padding:6px;                      "
                             "text-align:left"
"                   }"
"                   QPushButton:pressed{"
"                   background-color:rgba(255,255,255,255);"
"                   border-color:rgba(255,165,0,255);"
"                   color:rgba(255,165,0,255);"
                             "border-right:8px solid orange;"
                             "border-left:8px solid orange;"
                             "text-align:center;"
"                   }"
"                   QPushButton:hover{"
"                   background-color:rgba(255,255,255,255);"
"                   border-color:rgba(255,165,0,255);"
"                   color:rgba(255,165,0,255);"
                             "border-right:8px solid orange;"
                             "border-left:8px solid orange;"
                             "text-align:center;"
"                   }")

        self.setLayout(self.whole_layout)

        self.setWindowFlags(Qt.FramelessWindowHint)  # 影藏窗口
        self.showFullScreen()
        # self.setGeometry(0, 0, 1048, 890)


class NoteTable(QWidget):
    """
    公告管理(教师)/查看公告(学生)--公告表格
    教师权限：查删｜学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件
        self.l_current_note = QPushButton(u"最新公告")
        self.l_current_note.setEnabled(False)
        self.l_previous_note = QPushButton(u"过期公告")
        self.l_previous_note.setEnabled(False)
        self.bt_insert = QPushButton(u'添加新公告')
        self.lay.addWidget(self.l_current_note, 0, 0, 2, 1)
        self.lay.addWidget(self.bt_insert, 0, 4, 2, 1)
        self.lay.addWidget(self.l_previous_note, 0, 5, 2, 1)
        # 最后self添加布局
        self.setLayout(self.lay)
        self.setUpCSS()

    def setUpCSS(self):
        """
        添加样式
        :return: None
        """

        map(lambda x: x.setObjectName("note_label"), [self.l_previous_note, self.l_current_note])
        self.bt_insert.setObjectName("bt_insert")
        self.setStyleSheet('''
            QPushButton#note_label{
                font: 24px;
                color:black;
                border:none;
                background-color:white;
                border-left: 10px solid orange;
                border-bottom:2px solid orange;
            }
            
            QPushButton#bt_insert{
                background-color:orange;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:white;
                font: bold 18px;
            }
            
            QPushButton#bt_insert:hover{
                background-color:white;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:orange;
                font: bold 18px;
            }
            
            QPushButton#bt_insert:pressed{
                background-color:white;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:orange;
                font: bold 18px;
            }
        ''')


class NoteDetail(QDialog):
    """
    点击公告表后弹出公告详情窗口(所有用户)/添加新公告窗口(教师)
    教师权限：增(查改) | 学生权限：查
    """

    def __init__(self):
        QDialog.__init__(self)
        self.note_layout = QGridLayout()
        self.l_title = QLabel()
        self.l_title.setText(u"标题:")
        self.l_date = QLabel()
        self.l_date.setText(u"发布日期:")
        self.l_detail = QLabel()
        self.l_detail.setText(u"公告内容:")
        self.d_id = QLabel()
        self.d_is_valid = QLabel()
        self.d_title = QLineEdit()
        self.d_date = QLabel()
        self.d_detail = QTextEdit()
        self.bt_close = QPushButton(u"关闭")
        self.bt_update = QPushButton(u"修改")
        self.bt_insert = QPushButton(u"添加")

        self.note_layout.addWidget(self.l_title, 0, 0, 1, 1)
        self.note_layout.addWidget(self.d_title, 0, 1, 1, 3)
        self.note_layout.addWidget(self.l_date, 1, 0, 1, 1)
        self.note_layout.addWidget(self.d_date, 1, 1, 1, 3)
        self.note_layout.addWidget(self.l_detail, 2, 0, 1, 1)
        self.note_layout.addWidget(self.d_detail, 3, 0, 3, 4)
        self.note_layout.addWidget(self.bt_close, 6, 3, 1, 1)
        self.note_layout.addWidget(self.bt_insert, 6, 2, 1, 1)
        self.note_layout.addWidget(self.bt_update, 6, 1, 1, 1)
        self.note_layout.addWidget(self.d_id, 7, 0, 1, 1)
        self.note_layout.addWidget(self.d_is_valid, 7, 1, 1, 1)

        self.setLayout(self.note_layout)
        self.setUpCSS()

    def setUpCSS(self):
        self.setStyleSheet('''
            QLabel{
                background-color:rgba(255,165,0,200);
                border-style:outset;
                border-width:4px;
                border-radius:10px;
                border-color:rgba(255,255,255,30);
                font:bold 15px;
                color:rgb(255,255,255);
                padding:6px;
                text-align: center;
            }
            
            QPushButton{
                background-color:orange;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:white;
                font: bold 18px;
            }
            
            QPushButton:hover{
                background-color:white;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:orange;
                font: bold 18px;
            }
            
            QPushButton:pressed{
                background-color:white;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:orange;
                font: bold 18px;
            }
            
            QLineEdit{
                background-color:rgba(255,165,0,200);
                font: bold 15px;
                height:30px;
                border-radius:5px;
                color:white;
            }
            
            QTextEdit{
                background-color:rgba(255,165,0,200);
                font: bold 18px;
                height:30px;
                border-radius:5px;
                color:white;
            }
        ''')
        self.d_is_valid.hide()
        self.d_id.hide()

        self.resize(400, 300)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 影藏窗口


class StuffTable(QWidget):
    """
    人事管理(教师)--人事信息表格
    教师权限：查删
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件
        self.l_user = QPushButton(u"用户信息")
        self.l_user.setEnabled(False)
        self.bt_insert = QPushButton(u'添加新用户')
        self.lay.addWidget(self.l_user, 0, 0, 2, 1)
        self.lay.addWidget(self.bt_insert, 0, 4, 2, 1)
        # 最后self添加布局
        self.setLayout(self.lay)
        self.setUpCSS()

    def setUpCSS(self):
        """
        添加样式
        :return: None
        """

        self.l_user.setObjectName("user_label")
        self.bt_insert.setObjectName("bt_insert")
        self.setStyleSheet('''
                    QPushButton#user_label{
                        font: 24px;
                        color:black;
                        border:none;
                        background-color:white;
                        border-left: 10px solid orange;
                        border-bottom:2px solid orange;
                    }

                    QPushButton#bt_insert{
                        background-color:orange;
                        border: 2px solid orange;
                        border-radius:5px;
                        margin-right:30px;
                        color:white;
                        font: bold 18px;
                    }

                    QPushButton#bt_insert:hover{
                        background-color:white;
                        border: 2px solid orange;
                        border-radius:5px;
                        margin-right:30px;
                        color:orange;
                        font: bold 18px;
                    }

                    QPushButton#bt_insert:pressed{
                        background-color:white;
                        border: 2px solid orange;
                        border-radius:5px;
                        margin-right:30px;
                        color:orange;
                        font: bold 18px;
                    }
                ''')


class StuffDetail(QDialog):
    """
    点击人事表格后弹窗显示个人信息和个人总体考勤统计(教师)|添加人事信息窗口(教师)
    教师权限：增查改
    """

    def __init__(self):
        QDialog.__init__(self)
        self.user_layout = QGridLayout()
        self.l_user_id = QLabel()
        self.l_user_id.setText(u"学号|工号:")
        self.l_grade_class = QLabel()
        self.l_grade_class.setText(u"班级:")
        self.l_user_type = QLabel()
        self.l_user_type.setText(u"用户类型:")
        self.l_tel = QLabel()
        self.l_tel.setText(u"联系电话:")
        self.l_email = QLabel()
        self.l_email.setText(u"邮箱地址:")
        self.d_user_id = QLineEdit()
        self.d_user_id.setEnabled(False)
        self.d_major = QLineEdit()
        self.d_user_type = QComboBox()
        self.d_user_type.addItem(u"学生", 0)
        self.d_user_type.addItem(u"教师", 1)
        self.d_user_type.setCurrentIndex(0)
        self.d_grade = QLineEdit()
        self.d_grade.setPlaceholderText(u"年级")
        self.d_class = QLineEdit()
        self.d_class.setPlaceholderText(u"班")
        self.d_major = QLineEdit()
        self.d_major.setPlaceholderText(u"专业")
        self.d_tel = QLineEdit()
        self.d_email = QLineEdit()
        self.bt_close = QPushButton(u"关闭")
        self.bt_update = QPushButton(u"修改")
        self.bt_insert = QPushButton(u"添加")

        def setWeb(obj):
            obj.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)  # 取消滚动条
            obj.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
            obj.setFixedSize(500, 500)

        self.timestamp = QWebView()
        self.timestamp_url = QUrl("file:///D:/Bingo/AI_WorkPlace/GraduationProject/GraduationProject/Client/test/self_aweek_workhour_perday.html")
        self.hour_everyday = QWebView()
        self.hour_everyday_url = QUrl("file:///D:/Bingo/AI_WorkPlace/GraduationProject/GraduationProject/Client/test/self_aweek_workhour_perday.html")
        setWeb(self.timestamp)
        setWeb(self.hour_everyday)
        self.timestamp.load(self.timestamp_url)
        self.hour_everyday.load(self.hour_everyday_url)

        self.user_layout.addWidget(self.l_user_id, 0, 0, 1, 1)
        self.user_layout.addWidget(self.d_user_id, 0, 1, 1, 3)
        self.user_layout.addWidget(self.l_user_type, 1, 0, 1, 1)
        self.user_layout.addWidget(self.d_user_type, 1, 1, 1, 1)
        self.user_layout.addWidget(self.l_grade_class, 2, 0, 1, 1)
        self.user_layout.addWidget(self.d_grade, 2, 1, 1, 1)
        self.user_layout.addWidget(self.d_major, 2, 2, 1, 2)
        self.user_layout.addWidget(self.d_class, 2, 4, 1, 1)
        self.user_layout.addWidget(self.l_tel, 3, 0, 1, 1)
        self.user_layout.addWidget(self.d_tel, 3, 1, 1, 3)
        self.user_layout.addWidget(self.l_email, 4, 0, 1, 1)
        self.user_layout.addWidget(self.d_email, 4, 1, 1, 3)
        self.user_layout.addWidget(self.bt_close, 5, 3, 1, 1)
        self.user_layout.addWidget(self.bt_insert, 5, 2, 1, 1)
        self.user_layout.addWidget(self.bt_update, 5, 1, 1, 1)
        self.user_layout.addWidget(self.timestamp, 6, 0, 6, 6)
        self.user_layout.addWidget(self.hour_everyday, 6, 6, 6, 6)
        self.setLayout(self.user_layout)
        self.setUpCSS()

    def setUpCSS(self):
        self.setStyleSheet('''
            QLabel{
                background-color:rgba(255,165,0,200);
                border-style:outset;
                border-width:4px;
                border-radius:10px;
                border-color:rgba(255,255,255,30);
                font:bold 15px;
                color:rgb(255,255,255);
                padding:6px;
                text-align: center;
            }

            QPushButton{
                background-color:orange;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:white;
                font: bold 18px;
            }

            QPushButton:hover{
                background-color:white;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:orange;
                font: bold 18px;
            }

            QPushButton:pressed{
                background-color:white;
                border: 2px solid orange;
                border-radius:5px;
                margin-right:30px;
                color:orange;
                font: bold 18px;
            }

            QLineEdit{
                background-color:rgba(255,165,0,200);
                font: bold 15px;
                height:30px;
                border-radius:5px;
                color:white;
            }
            
            QComboBox{
                background-color:rgba(255,165,0,200);
                font: bold 18px;
                height:30px;
                border-radius:5px;
                color:white;
            }
            
        ''')

        self.setGeometry(500, 300, 800, 400)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 影藏窗口


class MyselfInfo(QWidget):
    """
    个人信息(学生)--个人信息展示
    学生权限：查改
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.myself_lay = QGridLayout()
        # 添加控件
        self.l_self = QPushButton(u"个人信息")
        self.l_self.setEnabled(False)
        self.l_user_id = QLabel()
        self.l_user_id.setText(u"学号:")
        self.l_grade_class = QLabel()
        self.l_grade_class.setText(u"班级:")
        self.l_user_type = QLabel()
        self.l_user_type.setText(u"用户类型:")
        self.l_tel = QLabel()
        self.l_tel.setText(u"联系电话:")
        self.l_email = QLabel()
        self.l_email.setText(u"邮箱地址:")
        self.d_user_id = QLineEdit()
        self.d_user_id.setEnabled(False)
        self.d_major = QLineEdit()
        self.d_user_type = QLabel()
        self.d_grade = QLineEdit()
        self.d_grade.setPlaceholderText(u"年级")
        self.d_class = QLineEdit()
        self.d_class.setPlaceholderText(u"班")
        self.d_major = QLineEdit()
        self.d_major.setPlaceholderText(u"专业")
        self.d_tel = QLineEdit()
        self.d_email = QLineEdit()
        self.bt_update = QPushButton(u"修改")

        self.myself_lay.addWidget(self.l_self, 1, 1, 1, 1)
        self.myself_lay.addWidget(self.l_user_id, 2, 2, 1, 1)
        self.myself_lay.addWidget(self.d_user_id, 2, 3, 1, 2)
        self.myself_lay.addWidget(self.l_user_type, 3, 2, 1, 1)
        self.myself_lay.addWidget(self.d_user_type, 3, 3, 1, 1)
        self.myself_lay.addWidget(self.l_grade_class, 4, 2, 1, 1)
        self.myself_lay.addWidget(self.d_grade, 4, 3,)
        self.myself_lay.addWidget(self.d_major, 4, 4,)
        self.myself_lay.addWidget(self.d_class, 4, 5,)
        self.myself_lay.addWidget(self.l_tel, 5, 2, 1, 1)
        self.myself_lay.addWidget(self.d_tel, 5, 3, 1, 3)
        self.myself_lay.addWidget(self.l_email, 6, 2, 1, 1)
        self.myself_lay.addWidget(self.d_email, 6, 3, 1, 3)
        self.myself_lay.addWidget(self.bt_update, 7, 5, 1, 2)

        # 最后self添加布局
        self.setLayout(self.myself_lay)
        self.setUpCSS()

    def setUpCSS(self):
        self.l_self.setObjectName("self_label")
        self.setStyleSheet('''
                QPushButton#self_label{
                        font: 24px;
                        color:black;
                        border:none;
                        background-color:white;
                        border-left: 10px solid orange;
                        border-bottom:2px solid orange;
                    }
                    
                QLabel{
                    background-color:rgba(255,165,0,200);
                    border-style:outset;
                    border-width:4px;
                    border-radius:10px;
                    border-color:rgba(255,255,255,30);
                    font:bold 15px;
                    color:rgb(255,255,255);
                    padding:6px;
                    text-align: center;
                }

                QPushButton{
                    background-color:orange;
                    border: 2px solid orange;
                    border-radius:5px;
                    margin-right:30px;
                    color:white;
                    font: bold 18px;
                }

                QPushButton:hover{
                    background-color:white;
                    border: 2px solid orange;
                    border-radius:5px;
                    margin-right:30px;
                    color:orange;
                    font: bold 18px;
                }

                QPushButton:pressed{
                    background-color:white;
                    border: 2px solid orange;
                    border-radius:5px;
                    margin-right:30px;
                    color:orange;
                    font: bold 18px;
                }

                QLineEdit{
                    background-color:rgba(255,165,0,200);
                    font: bold 15px;
                    height:30px;
                    border-radius:5px;
                    color:white;
                }
            ''')

        self.resize(300, 500)
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 影藏窗口


class GroupTable(QWidget):
    """
    分组管理(教师)--组别信息表格
    教师权限：查删
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class GroupDetail(QDialog):
    """
    点击分组表格后弹窗显示分组信息(教师)|添加分组信息窗口(教师)
    教师权限：增查改
    """

    def __init__(self):
        QDialog.__init__(self)


class MyGroup(QWidget):
    """
    查看分组(学生)--分组信息展示及其成员列表
    学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class AttendanceChart(QWidget):
    """
    考勤统计(所有用户)--考勤数据可视化图标，角色不同展示图表有差别
    教师权限：查｜学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class SourceTable(QWidget):
    """
    资源管理(教师)/查看资源(学生)--资源表格
    教师权限：查删｜学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class SourceDetail(QDialog):
    """
    点击资源表后弹出公资源情窗口(所有用户)/添加新资源窗口(教师)
    教师权限：增查改 | 学生权限：查
    """

    def __init__(self):
        QDialog.__init__(self)


class PermitTable(QWidget):
    """
    假条审批(教师)/假条管理(学生)--假条表格
    教师权限：查改(修改状态批准/拒绝)｜学生权限：查删
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class PermitDetail(QDialog):
    """
    点击假条表后弹出假条详情窗口(所有用户)/添加新假条窗口(学生)
    教师权限：查改(修改状态) | 学生权限：增查改(修改内容)
    """

    def __init__(self):
        QDialog.__init__(self)


class AchievementTable(QWidget):
    """
    成就管理(教师)/个人成就(学生)--成就表格
    教师权限：查删｜学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class AchievementDetail(QDialog):
    """
    点击成就表后弹出成就详情窗口(所有用户)/添加新成就窗口(教师)
    教师权限：增查改 | 学生权限：查
    """

    def __init__(self):
        QDialog.__init__(self)


class CompetitionTable(QWidget):
    """
    比赛管理(教师)/参与比赛(学生)--比赛表格
    教师权限：查删｜学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class CompetitionDetail(QDialog):
    """
    点击比赛表后弹出比赛详情窗口(所有用户)/添加新比赛窗口(教师)
    教师权限：增查改 | 学生权限：查
    """

    def __init__(self):
        QDialog.__init__(self)


class ProjectTable(QWidget):
    """
    项目管理(教师)/查看项目(学生)--项目表格
    教师权限：查删｜学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class ProjectDetail(QDialog):
    """
    点击项目表后弹出项目详情窗口(所有用户)/添加新项目窗口(教师)
    教师权限：增查改 | 学生权限：查
    """

    def __init__(self):
        QDialog.__init__(self)


class TaskArrangement(QWidget):
    """
    任务分配(教师)｜查看任务(学生)--任务表格
    教师权限：查改(是否完成)｜学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class TaskDetail(QDialog):
    """
    点击任务表后弹出项目详情窗口(所有用户)/添加新任务窗口(教师)
    教师权限：增查改 | 学生权限：查
    """

    def __init__(self):
        QDialog.__init__(self)


class SeatLocation(QWidget):
    """
    工位管理(教师)/查看工位(学生)--工位分部示意图
    教师权限：增查删｜学生权限：查
    """

    def __init__(self):
        QWidget.__init__(self)
        # 布局
        self.lay = QGridLayout()
        # 添加控件

        # 最后self添加布局
        self.setLayout(self.lay)


class SeatDetail(QDialog):
    """
    点击工位后弹出工位详情窗口(所有用户)
    教师权限：查改 | 学生权限：查
    """

    def __init__(self):
        QDialog.__init__(self)


class Pagination(QWidget):
    """
    基础数据表分页控件组合
    需要根据具体需求继承后重写
    在此仅定义必要静态样式和方法
    """

    def __init__(self):
        super(Pagination, self).__init__()
        # 布局管理器
        self.layout = QVBoxLayout()
        # 表格视图
        self.table = QTableWidget()
        self.table.setShowGrid(False)  # 不显示网格

        self.totalPageLabel = QLabel()
        self.currentPageLabel = QLabel()
        self.switchPageLineEdit = QLineEdit()
        self.switchPageLineEdit.setObjectName("ed_page")
        self.prevButton = QPushButton("Prev")
        self.prevButton.setObjectName("bt_page")
        self.nextButton = QPushButton("Next")
        self.nextButton.setObjectName("bt_page")
        self.switchPageButton = QPushButton("Switch")
        self.switchPageButton.setObjectName("bt_page")

        # 当前页
        self.currentPage = 1
        # 总页数
        self.totalPage = 1
        # 总记录数
        self.totalRecordCount = 0
        # 每页记录数
        self.pageRecordCount = 11

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可修改
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中时选一行
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.horizontalHeader().setFixedHeight(35)
        self.table.verticalHeader().setVisible(False)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout.addWidget(self.table)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.prevButton)
        hLayout.addWidget(self.nextButton)
        hLayout.addWidget(QLabel("跳转到"))
        self.switchPageLineEdit.setFixedWidth(40)
        hLayout.addWidget(self.switchPageLineEdit)
        hLayout.addWidget(QLabel("页"))
        hLayout.addWidget(self.switchPageButton)
        hLayout.addWidget(QLabel("当前页："))
        hLayout.addWidget(self.currentPageLabel)
        hLayout.addWidget(QLabel("总页数："))
        hLayout.addWidget(self.totalPageLabel)
        hLayout.addStretch(1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setObjectName("line")

        self.layout.addWidget(line)
        self.layout.addLayout(hLayout)
        self.setLayout(self.layout)
        self.resize(200, 300)

        self.setUpCSS()

    def setUpCSS(self):
        """
        美化控件,必要时先设置ObjectName
        :return:None
        """

        self.setStyleSheet('''
            QPushButton#bt_page{
                background-color:white;
                border: 3px solid orange;
                border-radius:5px;
                color:orange;
            }
            QLineEdit#ed_page{
                border:3px solid orange;
                color:orange;
            }
            #line{
                background-color:orange;
                border:none;
            }
            QTableWidget{
                border:none;
            }
            QHeaderView::section{
                background-color:orange;
                color:white;
                border:none;
            }
            QTableWidget::item{
                border-bottom:2px solid orange;
            }
            ''')


class OperationButtonInTable(QPushButton):

    def __init__(self, color='LightCoral', name=u'操作'):
        QPushButton.__init__(self)
        self.setText(name)
        self.setStyleSheet('''
            QPushButton{
                text-align : center;
                background-color : %(color)s;
                border: 3px solid %(color)s;
                border-radius:5px;
                font : bold 18px;
                color: white;
            }
            QPushButton:pressed{
                text-align : center;
                background-color : white;
                border: 3px solid %(color)s;
                border-radius:5px;
                font : bold 18px;
                color: %(color)s;
            }
            QPushButton:hover{
                text-align : center;
                background-color : white;
                border: 3px solid %(color)s;
                border-radius:5px;
                font : bold 18px;
                color: %(color)s;
            }
        ''' % ({'color': color}))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MyselfInfo()
    win.show()
    sys.exit(app.exec_())