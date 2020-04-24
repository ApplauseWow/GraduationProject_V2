# -*-coding:utf-8-*-
import sys
import time
import datetime
import os
from PyQt5.QtGui import QImage

from ui_design.ui_finish import *
from TypesEnum import *
from ClientRequest import CR
from TableColumnDict import TABLE_COLUMN_DICT
from ColumnMapper import Index2ColName, ColName2Index


class Alert(WarningWindow):
    """
    警告提醒窗
    """

    def __init__(self, words=None, _type=None):
        super(Alert, self).__init__()
        if words:
            self.words.setText(words)
        else:
            pass
        if _type == 'alright':
            self.pix = QPixmap('./ui_design/alright.png').scaled(100, 100)
            self.warning.setPixmap(self.pix)
        # 设置定时器
        self.time_count = QTimer()
        self.time_count.setInterval(800)
        self.time_count.start()
        self.time_count.timeout.connect(self.timeout_close)

    def timeout_close(self):
        """
        倒计时关闭此窗口
        :return: None
        """

        self.close()


class Page(Pagination):
    """
    数据表分页，构建基本事件响应函数
    Management中多个控件需要重写此类
    """

    def __init__(self):
        Pagination.__init__(self)
        # 在继承重写后再执行以下初始化函数

    def setUpConnect(self):
        """
        添加按钮槽函数
        :return:
        """
        self.prevButton.clicked.connect(self.onPrevPage)
        self.nextButton.clicked.connect(self.onNextPage)
        self.switchPageButton.clicked.connect(self.onSwitchPage)
        self.table.doubleClicked.connect(self.showRecord)

    def initializedModel(self):
        """
        初始化界面数据，待重写
        :return:
        """

        pass

    def queryRecord(self, limitIndex):
        """
        根据分页查询记录，待重写
        :param limitIndex:开头记录位置
        :return:
        """

        pass

    def onPrevPage(self):
        """
        上一页
        :return:
        """

        self.currentPage -= 1
        limitIndex = (self.currentPage - 1) * self.pageRecordCount
        self.queryRecord(limitIndex)
        self.updateStatus()

    def onNextPage(self):
        """
        下一页
        :return:
        """

        self.currentPage += 1
        limitIndex = (self.currentPage - 1) * self.pageRecordCount
        self.queryRecord(limitIndex)
        self.updateStatus()

    def onSwitchPage(self):
        """
        切换到指定页面
        :return:
        """

        szText = self.switchPageLineEdit.text()
        pattern = re.compile('^[0-9]+$')
        match = pattern.match(szText)
        if not match:
            # QMessageBox.information(self, "提示", "请输入数字.")
            msg = Alert(words=u"请输入数字")
            msg.exec_()
            return
        if szText == "":
            # QMessageBox.information(self, "提示", "请输入跳转页面.")
            msg = Alert(words=u"请输入跳转页面")
            msg.exec_()
            return
        pageIndex = int(szText)
        if pageIndex > self.totalPage or pageIndex < 1:
            # QMessageBox.information(self, "提示", "没有指定的页，清重新输入.")
            msg = Alert(words=u"没有此页")
            msg.exec_()
            return
        if pageIndex == self.currentPage:  # 就是当前页面
            # 直接返回，避免不必要的查询开销
            return
        limitIndex = (pageIndex - 1) * self.pageRecordCount
        self.queryRecord(limitIndex)
        self.currentPage = pageIndex
        self.updateStatus()

    def updateStatus(self):
        """
        更新控件状态
        :return:
        """

        self.currentPageLabel.setText(str(self.currentPage))
        self.totalPageLabel.setText(str(self.totalPage))
        if self.currentPage <= 1:
            self.prevButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)

        if self.currentPage >= self.totalPage:
            self.nextButton.setEnabled(False)
        else:
            self.nextButton.setEnabled(True)

    def showRecord(self, index):
        """
        双击表格显示具体记录信息，待重写
        :return:
        """

        pass

    def addRecords(self, col_list, data):
        """
        添加记录
        :param col_list:[(colname, is_hidden, is_pk), ...]
        :return: None
        """

        # self.table.clearContents()  # 清空内容
        # 非常奇怪表格行不能顺序删除不然会莫名其妙的错误，必须逆序删除，so interesting～～!?!?
        map(lambda x: self.table.removeRow(x), range(self.table.rowCount())[::-1])
        self.table.setColumnCount(len(col_list))
        # 无需设置固定行数，利用insertRow动态添加
        # self.table.setRowCount(self.pageRecordCount)
        self.table.setHorizontalHeaderLabels(map(lambda x: x['name'], col_list))  # 设置表头
        map(lambda x: self.table.setColumnHidden(x[0], x[1]['is_hidden']), enumerate(col_list))  # 隐藏某些列
        for num_r, row in enumerate(data):
            self.table.insertRow(num_r)
            pk = []
            self.table.setRowHeight(num_r, 50)
            for num_c, col in enumerate(col_list):
                if col['is_pk']:  # 添加主键
                    pk.append(row[num_c])
                if col['name'] == u'操作':  # 操作栏
                    self.table.setCellWidget(num_r, num_c, self.addOperationButton(pk))
                else:  # 普通字段
                    if col.has_key('convert'):
                        item = QTableWidgetItem(u"{}".format(col['convert'](row[num_c])))
                    else:
                        item = QTableWidgetItem(u"{}".format(row[num_c] if row[num_c] else ""))  # 注意中文编码
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.table.setItem(num_r, num_c, item)

    def addOperationButton(self, primary_key):
        """
        添加操作按钮，待重写
        :return:
        """
        widget = QWidget()
        bt = OperationButtonInTable(name=u'删除')
        bt.clicked.connect(lambda: self.operationOnBtClicked(primary_key))
        hLayout = QHBoxLayout()
        hLayout.addWidget(bt)
        widget.setLayout(hLayout)
        return widget

    def operationOnBtClicked(self, primary_key):
        """
        操作按钮槽函数，待重写
        :param primary_key:　主键
        :return:
        """

        pass


# 系统前端主界面即考勤界面，内部组件抽象为内部类包含注册界面，验证界面
class SysHome(MainWindow):
    """
    主界面
    """

    def __init__(self):
        super(SysHome, self).__init__()

        # 设置定时器
        self.timer_clock = QTimer()
        self.timer_clock.setInterval(1000)
        self.timer_clock.start()
        self.timer_clock.timeout.connect(self.update_time)

    def update_time(self):
        """
        更新时间
        :return:None
        """

        self.clock.display(time.strftime("%X", time.localtime()))

    class Register(RegisterWindow):
        """
        人脸注册窗口
        """

        def __init__(self):
            RegisterWindow.__init__(self)

    class MyInfo(InfoWindow):
        """
        考勤窗口｜个人信息显示窗口
        """

        def __init__(self):
            InfoWindow.__init__(self)


class Management(ManagementWindow):
    """
    资源管理窗口
    """

    def __init__(self, user_id, user_type):
        ManagementWindow.__init__(self, user_id, user_type)
        # 添加顺序一定按照按钮顺序
        self.page_one = self.ShowUsers(user_id=user_id, user_type=user_type) if UserType(
            user_type) == UserType.Teacher else self.ShowMyself(user_id=user_id, user_type=user_type)
        self.page_two = self.ShowNotes(user_id=user_id, user_type=user_type)

        self.right_layout.addWidget(self.page_one)
        self.right_layout.addWidget(self.page_two)

        self.setUpConnect()

    def setUpConnect(self):
        """
        绑定按钮槽函数
        :return: None
        """

        map(lambda x: x.clicked.connect(self.switchPage), self.bts)

    def switchPage(self):
        """
        点击菜单按钮后切换页面
        :return: None
        """

        # 可能与其他sender冲突
        try:
            index = self.menu_dict[self.sender().objectName()]
            self.right_layout.setCurrentIndex(index)
            self.right_layout.widget(index).initPage()  # 所有组内控件重写一个初始化函数解决了堆叠控件切换后刷新问题
        except Exception as e:
            print(e)
            warning = Alert(words=u"切换失败！")
            warning.exec_()

    # 以下为内部组件类 所有init函数参数都必须统一接收user_id user_type 注意顺序
    class ShowNotes(NoteTable):
        """
        继承NoteTable封装业务逻辑
        数据需求：未过期公告序列｜过期公告序列
        描述：【教师】两个表格分别为过期公告和未过期公告表
    　　　    【学生】一个表格未过期公告表
        """

        def __init__(self, user_id, user_type):
            NoteTable.__init__(self)
            self.user_type = user_type
            self.user_id = user_id
            if UserType(user_type) == UserType.Teacher:  # 教师
                self.current_note = self.CurrentNote(user_type)
                self.lay.addWidget(self.current_note, 2, 0, 5, 5)  # 未过期公告表
                self.previous_note = self.PreviousNote(user_type)
                self.lay.addWidget(self.previous_note, 2, 5, 5, 5)  # 过期公告表
                self.current_note.update_signal.connect(self.initPage)
                self.lay.setRowStretch(1, 1)
                self.lay.setRowStretch(3, 4)
                self.lay.setRowStretch(7, 1)
                self.bt_insert.clicked.connect(lambda: self.createANoteDetail(user_type, None))
            elif UserType(user_type) == UserType.Student:  # 学生
                self.current_note = self.CurrentNote(user_type)
                self.lay.addWidget(self.current_note, 2, 0, 5, 5)
                self.bt_insert.hide()
                self.l_previous_note.hide()
                self.lay.setRowStretch(1, 1)
                self.lay.setRowStretch(3, 4)
                self.lay.setRowStretch(7, 1)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            if UserType(self.user_type) == UserType.Teacher:
                self.previous_note.initializedModel()
                self.previous_note.updateStatus()
            self.current_note.initializedModel()
            self.current_note.updateStatus()

        def createANoteDetail(self, user_type, data):
            """
            创建一个公告详情
            :return: None
            """

            win = self.ANote(user_type, data)
            win.update_signal.connect(self.initPage)
            win.exec_()

        class CurrentNote(Page):
            """
            未过期的公告表
            """

            update_signal = pyqtSignal()  # 更新过期公告信号

            def __init__(self, user_type):
                Page.__init__(self)
                self.user_type = user_type
                self.col_list = TABLE_COLUMN_DICT[UserType(user_type)]['current_note']  # 获取表头信息
                self.initializedModel()
                self.setUpConnect()
                self.updateStatus()

            def initializedModel(self):
                try:
                    conn = CR()
                    self.currentPage = 1
                    self.totalRecordCount = conn.GetCountRequest('note', {'is_valid': NoteStatus.Valid.value})
                    conn.CloseChannel()
                    if self.totalRecordCount % self.pageRecordCount == 0:
                        if self.totalRecordCount != 0:
                            self.totalPage = self.totalRecordCount / self.pageRecordCount
                        else:
                            self.totalPage = 1
                    else:
                        self.totalPage = int(self.totalRecordCount / self.pageRecordCount) + 1
                    self.queryRecord(0)
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"查询失败！")
                    warning.exec_()

            def queryRecord(self, limit_index):
                """
                重写查询记录
                :param limit_index:从第limitIndex条开始
                :return:
                """

                try:
                    conn = CR()
                    notes = conn.GetAllNotesRequest(start=limit_index, num=self.pageRecordCount,
                                                    is_valid=NoteStatus.Valid.value)
                    self.addRecords(self.col_list, notes)
                    conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"查询失败！")
                    warning.exec_()

            def operationOnBtClicked(self, primary_key):
                """
                重写操作按钮
                :param primary_key: 主键
                :return: None
                """

                try:
                    conn = CR()
                    # 更新
                    res = conn.VoidTheNoteRequest(primary_key)
                    if res == ClientRequest.Success:
                        alright = Alert(words=u"操作成功！", _type='alright')
                        alright.exec_()
                        self.update_signal.emit()  # 更新页面
                    conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"操作失败！")
                    warning.exec_()

            def showRecord(self, index):
                """
                重写双击记录信号的槽函数
                :param index: index.row(), index.column()
                :return:None
                """

                row = index.row()
                col = self.table.columnCount()
                data = {}
                for c in range(col):
                    item = self.table.item(row, c)
                    if isinstance(item, QTableWidgetItem):  # 是数据
                        data[Index2ColName['note'][c]] = item.text()
                    else:  # 不是数据
                        pass
                # 弹窗查看
                note_detail = Management.ShowNotes.ANote(self.user_type, data)
                note_detail.update_signal.connect(lambda: self.update_signal.emit())
                note_detail.exec_()

        class PreviousNote(Page):
            """
            过期的公告表
            """

            def __init__(self, user_type):
                Page.__init__(self)
                self.user_type = user_type
                self.col_list = TABLE_COLUMN_DICT[UserType(user_type)]['previous_note']  # 获取表头信息
                self.initializedModel()
                self.setUpConnect()
                self.updateStatus()

            def initializedModel(self):
                try:
                    conn = CR()
                    self.currentPage = 1
                    self.totalRecordCount = conn.GetCountRequest('note', {'is_valid': NoteStatus.Invalid.value})
                    conn.CloseChannel()
                    if self.totalRecordCount % self.pageRecordCount == 0:
                        if self.totalRecordCount != 0:
                            self.totalPage = self.totalRecordCount / self.pageRecordCount
                        else:
                            self.totalPage = 1
                    else:
                        self.totalPage = int(self.totalRecordCount / self.pageRecordCount) + 1
                    self.queryRecord(0)
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"查询失败！")
                    warning.exec_()

            def queryRecord(self, limitIndex):
                """
                重写查询记录
                :param limitIndex:从第limitIndex条开始
                :return:
                """

                try:
                    conn = CR()
                    notes = conn.GetAllNotesRequest(start=limitIndex, num=self.pageRecordCount,
                                                    is_valid=NoteStatus.Invalid.value)
                    self.addRecords(self.col_list, notes)
                    conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"查询失败！")
                    warning.exec_()

            def showRecord(self, index):
                """
                重写双击记录信号的槽函数
                :param index: index.row(), index.column()
                :return:None
                """

                row = index.row()
                col = self.table.columnCount()
                data = {}
                for c in range(col):
                    item = self.table.item(row, c)
                    if isinstance(item, QTableWidgetItem):  # 是数据
                        data[Index2ColName['note'][c]] = item.text()
                    else:  # 不是数据
                        pass
                # 弹窗查看
                note_detail = Management.ShowNotes.ANote(self.user_type, data)
                note_detail.bt_insert.hide()
                note_detail.bt_update.hide()
                note_detail.d_title.setEnabled(False)
                note_detail.d_detail.setEnabled(False)
                note_detail.exec_()

        class ANote(NoteDetail):
            """
            公告详情 | 添加/修改公告　窗口
            """

            update_signal = pyqtSignal()  # 更新未过期公告栏信号

            def __init__(self, user_type, data=None):
                NoteDetail.__init__(self)
                if UserType(user_type) == UserType.Student:  # 学生
                    self.bt_update.hide()
                    self.bt_insert.hide()
                    self.d_title.setEnabled(False)
                    self.d_detail.setEnabled(False)
                else:  # 教师
                    pass
                if not data:  # 插入
                    self.l_date.hide()
                    self.d_date.hide()
                    self.bt_update.hide()
                else:  # 查看或者修改
                    self.bt_insert.hide()
                    self.d_title.setText(data['title'])
                    self.d_date.setText(data['pub_date'])
                    self.d_detail.setText(data['detail'])
                    self.d_id.setText(data['note_id'])
                    self.d_is_valid.setText(data['is_valid'])

                self.bt_insert.clicked.connect(self.CreateNewNote)
                self.bt_update.clicked.connect(self.ModifyNote)
                self.bt_close.clicked.connect(self.close)

            def CreateNewNote(self):
                """
                创建新公告
                :return: None
                """

                t = time.localtime(time.time())
                data = {
                    'title': self.d_title.text(),
                    'detail': self.d_detail.toPlainText(),
                    'pub_date': datetime.date(*(t.tm_year, t.tm_mon, t.tm_mday)),
                    'is_valid': NoteStatus.Valid.value
                }
                try:
                    conn = CR()
                    res = conn.InsertANoteRequest(data)
                    if res == ClientRequest.Success:
                        alright = Alert(words=u"操作成功！", _type='alright')
                        alright.exec_()
                        self.update_signal.emit()
                    conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"操作失败！")
                    warning.exec_()
                finally:
                    self.close()

            def ModifyNote(self):
                """
                修改公告
                :return:None
                """

                t = time.localtime(time.time())
                data = {
                    'title': self.d_title.text(),
                    'detail': self.d_detail.toPlainText(),
                    'pub_date': datetime.date(*(t.tm_year, t.tm_mon, t.tm_mday)),
                    'note_id': int(self.d_id.text())
                }
                try:
                    conn = CR()
                    res = conn.ModifyTheNoteRequest(data)
                    if res == ClientRequest.Success:
                        alright = Alert(words=u"操作成功！", _type='alright')
                        alright.exec_()
                        self.update_signal.emit()
                    conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"操作失败！")
                    warning.exec_()
                finally:
                    self.close()

    # ---------------------ShowNote  complete------------------------

    class ShowUsers(StuffTable):
        """
        继承StuffTable封装业务逻辑
        数据需求：所有用户信息
        描述：【教师】一个用户表格
        """

        def __init__(self, user_id, user_type):
            StuffTable.__init__(self)
            self.user_table = self.UserTable(user_type)
            self.user_table.update_signal.connect(self.initPage)
            self.lay.addWidget(self.user_table, 3, 1, 5, 5)
            self.lay.setRowStretch(1, 1)
            self.lay.setRowStretch(3, 4)
            self.lay.setRowStretch(7, 1)
            self.lay.setColumnStretch(1, 1)
            self.lay.setColumnStretch(3, 2)
            self.lay.setColumnStretch(7, 1)
            self.bt_insert.clicked.connect(lambda: self.createAUserDetail(None))

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            self.user_table.initializedModel()
            self.user_table.updateStatus()

        def createAUserDetail(self, data):
            """
            创建一个用户信息窗口
            :return: None
            """

            win = self.AUser(data)
            win.update_signal.connect(self.initPage)
            win.exec_()

        class UserTable(Page):
            """
            用户表
            """

            update_signal = pyqtSignal()

            def __init__(self, user_type):
                Page.__init__(self)
                self.user_type = user_type
                self.col_list = TABLE_COLUMN_DICT[UserType(user_type)]['user']  # 获取表头信息
                self.initializedModel()
                self.setUpConnect()
                self.updateStatus()

            def initializedModel(self):
                try:
                    conn = CR()
                    self.currentPage = 1
                    self.totalRecordCount = conn.GetCountRequest('user')
                    conn.CloseChannel()
                    if self.totalRecordCount % self.pageRecordCount == 0:
                        if self.totalRecordCount != 0:
                            self.totalPage = self.totalRecordCount / self.pageRecordCount
                        else:
                            self.totalPage = 1
                    else:
                        self.totalPage = int(self.totalRecordCount / self.pageRecordCount) + 1
                    self.queryRecord(0)
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"查询失败！")
                    warning.exec_()

            def queryRecord(self, limitIndex):
                """
                重写查询记录
                :param limitIndex:从第limitIndex条开始
                :return:
                """

                try:
                    conn = CR()
                    users = conn.GetAllUserRequest(start=limitIndex, num=self.pageRecordCount)
                    self.addRecords(self.col_list, users)
                    conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"查询失败！")
                    warning.exec_()

            def operationOnBtClicked(self, primary_key):
                """
                重写操作按钮
                :param primary_key: 主键
                :return: None
                """

                try:
                    conn = CR()
                    # 更新
                    res = conn.DeleteTheUserRequest(primary_key)
                    if res == ClientRequest.Success:
                        alright = Alert(words=u"操作成功！", _type='alright')
                        alright.exec_()
                        self.initializedModel()  # 重新刷新页面色
                        self.updateStatus()
                        self.update_signal.emit()
                    conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"操作失败！")
                    warning.exec_()

            def showRecord(self, index):
                """
                重写双击记录信号的槽函数
                :param index: index.row(), index.column()
                :return:None
                """

                row = index.row()
                col = self.table.columnCount()
                data = {}
                for c in range(col):
                    item = self.table.item(row, c)
                    if isinstance(item, QTableWidgetItem):  # 是数据
                        if Index2ColName['user'][c] == 'user_type':
                            mapper = {u"教师": UserType.Teacher.value, u"学生": UserType.Student.value}
                            data[Index2ColName['user'][c]] = mapper[item.text()]
                        else:
                            data[Index2ColName['user'][c]] = item.text()
                    else:  # 不是数据
                        pass
                # 弹窗查看
                user_detail = Management.ShowUsers.AUser(data)
                user_detail.update_signal.connect(lambda: self.update_signal.emit())
                user_detail.exec_()

        class AUser(StuffDetail):
            """
            用户详情 | 添加/修改用户信息
            """

            update_signal = pyqtSignal()  # 更新用户栏信号

            def __init__(self, data=None):
                StuffDetail.__init__(self)
                if not data:  # 插入
                    self.bt_update.hide()
                    self.d_user_id.setEnabled(True)
                    self.timestamp.hide()
                    self.hour_everyday.hide()
                else:  # 查看或者修改
                    self.bt_insert.hide()
                    self.d_user_id.setText(data['user_id'])
                    self.d_major.setText(data['major'])
                    self.d_user_type.setCurrentIndex(data['user_type'])
                    self.d_grade.setText(data['grade'])
                    self.d_class.setText(data['_class'])
                    self.d_tel.setText(data['tel'])
                    self.d_email.setText(data['email'])
                    self.isTeacher(None)
                    if UserType(int(data['user_type'])) == UserType.Student:
                        self.initCharts(int(data['user_id']))

                self.d_user_type.activated.connect(self.isTeacher)
                self.bt_insert.clicked.connect(self.CreateNewUser)
                self.bt_update.clicked.connect(self.ModifyUser)
                self.bt_close.clicked.connect(self.close)

            def initCharts(self, user_id):
                """
                初始化考勤统计图表
                :return:
                """

                data = {'user_id': user_id}
                try:
                    # 查询数据
                    conn = CR()
                    res_everyday_hour = conn.GetWorkHourEverYDayRequest(data)
                    res_timestamp = conn.GetClockInOrOutTimeStampRequest(data)
                    conn.CloseChannel()
                    # 创建js文件
                    with open('./ui_design/js/html_model.html', 'r') as f:
                        html_head = f.read()
                    with open('./ui_design/js/self_clockInOrOut_distribution.js', 'r') as f:
                        js_timestamp = f.read()
                    with open('./ui_design/js/self_everyday_workhour_aweek.js', 'r') as f:
                        js_everyday_hour = f.read()
                    html_timestamp = "".join([html_head.format(400, 400),
                                              "<script>var data_clockin = {};var data_clockout = {};</script>".format(
                                                  res_timestamp['clock_in'], res_timestamp['clock_out']),
                                              "<script>",
                                              js_timestamp,
                                              "</script></body></html>"])
                    html_everyday_hour = "".join([html_head.format(400, 400),
                                                  "<script>var data = {};</script>".format(res_everyday_hour),
                                                  "<script>",
                                                  js_everyday_hour,
                                                  "</script></body></html>"])
                    with open('./ui_design/html_cache/self_1.html', 'w') as f:
                        f.write(html_timestamp)
                    with open('./ui_design/html_cache/self_2.html', 'w') as f:
                        f.write(html_everyday_hour)

                    current_path = os.getcwd()  # 当前目录
                    # 加载网页
                    self.timestamp_url.setUrl(
                        "file:///" + os.path.join(current_path, "ui_design", "html_cache", "self_1.html").replace('\\',
                                                                                                                  '/'))
                    self.timestamp.setUrl(self.timestamp_url)
                    self.hour_everyday_url.setUrl(
                        "file:///" + os.path.join(current_path, "ui_design", "html_cache", "self_2.html").replace('\\',
                                                                                                                  '/'))
                    self.hour_everyday.setUrl(self.hour_everyday_url)
                except Exception as e:
                    print(e)
                    warning = Alert(words=u" 统计失败！")
                    warning.exec_()
                finally:
                    self.close()

            def CreateNewUser(self):
                """
                创建新公告
                :return: None
                """

                if self.checkInput():
                    data = {
                        'user_id': int(self.d_user_id.text()),
                        'user_type': self.d_user_type.currentData(),
                        'major': self.d_major.text() if UserType(
                            self.d_user_type.currentData()) == UserType.Student else None,
                        'grade': int(self.d_grade.text()) if UserType(
                            self.d_user_type.currentData()) == UserType.Student else None,
                        '_class': int(self.d_class.text()) if UserType(
                            self.d_user_type.currentData()) == UserType.Student else None,
                        'tel': int(self.d_tel.text()),
                        'email': self.d_email.text()
                    }
                    try:
                        conn = CR()
                        res = conn.InsertAUserRequest(data)
                        if res == ClientRequest.Success:
                            alright = Alert(words=u"操作成功！", _type='alright')
                            alright.exec_()
                            self.update_signal.emit()
                        conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"操作失败！")
                        warning.exec_()
                    finally:
                        self.close()
                else:  # 非法输入
                    pass

            def ModifyUser(self):
                """
                修改公告
                :return:None
                """

                if self.checkInput():
                    data = {
                        'user_id': int(self.d_user_id.text()),
                        'user_type': self.d_user_type.currentData(),
                        'major': self.d_major.text() if UserType(
                            self.d_user_type.currentData()) == UserType.Student else None,
                        'grade': int(self.d_grade.text()) if UserType(
                            self.d_user_type.currentData()) == UserType.Student else None,
                        '_class': int(self.d_class.text()) if UserType(
                            self.d_user_type.currentData()) == UserType.Student else None,
                        'tel': int(self.d_tel.text()),
                        'email': self.d_email.text()
                    }
                    try:
                        conn = CR()
                        res = conn.ModifyTheUserRequest(data)
                        if res == ClientRequest.Success:
                            alright = Alert(words=u"操作成功！", _type='alright')
                            alright.exec_()
                            self.update_signal.emit()
                        conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"操作失败！")
                        warning.exec_()
                    finally:
                        self.close()
                else:  # 非法输入
                    pass

            def isTeacher(self, index):
                """
                下拉框根据所选角色类型隐藏班级专业
                :return:
                """

                if UserType(self.d_user_type.currentData()) == UserType.Teacher:
                    self.d_major.hide()
                    self.d_grade.hide()
                    self.d_class.hide()
                    self.l_grade_class.hide()
                else:
                    self.d_major.show()
                    self.d_grade.show()
                    self.d_class.show()
                    self.l_grade_class.show()

            def checkInput(self):
                """
                检查非法输入
                :return:
                """

                checks = [self.d_user_id, self.d_grade, self.d_major, self.d_class, self.d_tel,
                          self.d_email] if UserType(self.d_user_type.currentData()) == UserType.Student else [
                    self.d_user_id, self.d_tel, self.d_email]
                for sz in checks:
                    szText = sz.text()
                    if sz is self.d_major or sz is self.d_email:
                        szText = szText.strip()  # 去掉头尾空格
                    else:
                        pattern = re.compile('^[0-9]+$')
                        match = pattern.match(szText)
                        if not match:
                            # QMessageBox.information(self, "提示", "请输入数字.")
                            msg = Alert(words=u"请输入数字")
                            msg.exec_()
                            return False
                    if szText == "":
                        # QMessageBox.information(self, "提示", "请输入跳转页面.")
                        msg = Alert(words=u"输入不能为空")
                        msg.exec_()
                        return False
                else:
                    return True

    # ---------------------ShowUsers  complete------------------------

    class ShowMyself(MyselfInfo):
        """
        继承MyInfo封装业务逻辑
        数据需求：个人用户信息
        描述：【学生】一组信息
        """

        update_signal = pyqtSignal()  # 更新用户信息信号

        def __init__(self, user_id, user_type):
            MyselfInfo.__init__(self)
            self.user_id = user_id
            self.myself_lay.setRowStretch(0, 1)
            self.myself_lay.setRowStretch(2, 4)
            self.myself_lay.setRowStretch(10, 3)
            self.myself_lay.setColumnStretch(0, 1)
            self.myself_lay.setColumnStretch(9, 2)
            self.update_signal.connect(self.initPage)
            self.bt_update.clicked.connect(self.ModifySelfInfo)
            self.initPage()

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            try:
                conn = CR()
                data = {'user_id': self.user_id}
                Col2Index = ColName2Index['user']
                data = conn.GetSelfInfoRequest(data)
                conn.CloseChannel()
                self.d_user_id.setText(str(data[Col2Index['user_id']]))
                self.d_grade.setText(str(data[Col2Index['grade']]))
                self.d_major.setText(data[Col2Index['major']])
                self.d_class.setText(str(data[Col2Index['_class']]))
                self.d_tel.setText(str(data[Col2Index['tel']]))
                self.d_email.setText(data[Col2Index['email']])
                mapper = {UserType.Teacher.value: u"教师", UserType.Student.value: u"学生"}
                self.d_user_type.setText(mapper[data[Col2Index['user_type']]])
            except Exception as e:
                print(e)
                warning = Alert(words=u"查询失败！")
                warning.exec_()

        def ModifySelfInfo(self):
            """
            修改个人信息
            :return: None
            """

            if self.checkInput():
                mapper = {u"教师": UserType.Teacher.value, u"学生": UserType.Student.value}
                data = {
                    'user_id': int(self.d_user_id.text()),
                    'user_type': mapper[self.d_user_type.text()],
                    'major': self.d_major.text(),
                    'grade': int(self.d_grade.text()),
                    '_class': int(self.d_class.text()),
                    'tel': int(self.d_tel.text()),
                    'email': self.d_email.text()
                }
                try:
                    conn = CR()
                    res = conn.ModifyTheUserRequest(data)
                    if res == ClientRequest.Success:
                        alright = Alert(words=u"操作成功！", _type='alright')
                        alright.exec_()
                        self.update_signal.emit()
                    conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(words=u"操作失败！")
                    warning.exec_()
            else:  # 非法输入
                pass

        def checkInput(self):
            """
            检查非法输入
            :return:
            """

            checks = [self.d_grade, self.d_major, self.d_class, self.d_tel, self.d_email]
            for sz in checks:
                szText = sz.text()
                if sz is self.d_major or sz is self.d_email:
                    szText = szText.strip()
                else:
                    pattern = re.compile('^[0-9]+$')
                    match = pattern.match(szText)
                    if not match:
                        # QMessageBox.information(self, "提示", "请输入数字.")
                        msg = Alert(words=u"请输入数字")
                        msg.exec_()
                        return False
                if szText == "":
                    # QMessageBox.information(self, "提示", "请输入跳转页面.")
                    msg = Alert(words=u"输入不能为空")
                    msg.exec_()
                    return False
            else:
                return True

    # ---------------------ShowMyself  complete------------------------

    class ShowAttendanceCharts(AttendanceChart):
        """
        继承AttendanceChart封装业务逻辑
        数据需求：考勤记录处理后数据
        描述：【考勤记录相关处理结果】一组信息
        """

        def __init__(self, user_id, user_type):
            AttendanceChart.__init__(self)
            self.user_id = user_id
            self.user_type = user_type

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

        def createHTML(self):
            """
            创建图表页面
            :return:
            """

            try:
                # 查询数据
                conn = CR()
                if UserType(self.user_type) == UserType.Student:  # 学生个人考勤页面
                    data = {'user_id': self.user_id}
                    res_everyday_hour = conn.GetWorkHourEveryDayRequest(data)
                    res_timestamp = conn.GetClockInOrOutTimeStampRequest(data)
                    conn.CloseChannel()
                    # 创建js文件
                    with open('./ui_design/js/html_model.html', 'r') as f:
                        html_head = f.read()
                    with open('./ui_design/js/self_clockInOrOut_distribution.js', 'r') as f:
                        js_timestamp = f.read()
                    with open('./ui_design/js/self_everyday_workhour_aweek.js', 'r') as f:
                        js_everyday_hour = f.read()
                    html_timestamp = "".join([html_head.format(400, 400),
                                              "<script>var data_clockin = {};var data_clockout = {};</script>".format(
                                                  res_timestamp['clock_in'], res_timestamp['clock_out']),
                                              "<script>",
                                              js_timestamp,
                                              "</script></body></html>"])
                    html_everyday_hour = "".join([html_head.format(400, 400),
                                                  "<script>var data = {};</script>".format(res_everyday_hour),
                                                  "<script>",
                                                  js_everyday_hour,
                                                  "</script></body></html>"])
                else:  # 全体考勤页面
                    data = None
                    res_location = conn.GetClockInOrOutCountEachHourRequest(data)
                    data = {}
                    res_clockin_today = conn.GetClockInRateTodayRequest(data)
                    conn.CloseChannel()
                    # 创建js文件
                    with open('./ui_design/js/html_model.html', 'r') as f:
                        html_head = f.read()
                    with open('./ui_design/js/aweek_every_hour_clockIn.js', 'r') as f:
                        js_each_hour = f.read()
                    with open('./ui_design/js/today_clockIn_rate.js', 'r') as f:
                        js_everyday_hour = f.read()
                    html_clock_in = "".join([html_head.format(400, 400),
                                             "<script>var data = {};var label = {};</script>".format(
                                                 res_location['clock_in'], '到岗人数'),
                                             "<script>",
                                             js_each_hour,
                                             "</script></body></html>"])
                    html_clock_out = "".join([html_head.format(400, 400),
                                              "<script>var data = {};var label = {}</script>".format(
                                                  res_location['clock_out'], '离岗人数'),
                                              "<script>",
                                              js_each_hour,
                                              "</script></body></html>"])
                    html_clock_in_rate = "".join([html_head.format(400, 400),
                                                  "<script>var clock_in = {};var total = {}</script>".format(
                                                      res_clockin_today['clock_in'], res_clockin_today['total']),
                                                  "<script>",
                                                  js_each_hour,
                                                  "</script></body></html>"])
                with open('./ui_design/html_cache/self_1.html', 'w') as f:
                    f.write(html_timestamp)
                with open('./ui_design/html_cache/self_2.html', 'w') as f:
                    f.write(html_everyday_hour)
            except Exception as e:
                print(e)
                warning = Alert(words=u" 统计失败！")
                warning.exec_()
            finally:
                self.close()

        def initCharts(self):
            """
            初始化图表
            :return:
            """

            current_path = os.getcwd()  # 当前目录
            # 加载网页
            self.chart1_url.setUrl(
                "file:///" + os.path.join(current_path, "ui_design", "html_cache", "self_1.html").replace('\\',
                                                                                                          '/') if UserType(
                    self.user_type) == UserType.Student else
                "file:///" + os.path.join(current_path, "ui_design", "html_cache", "all_1.html").replace('\\',
                                                                                                         '/')
            )
            self.chart1.setUrl(self.chart1_url)
            self.chart2_url.setUrl(
                "file:///" + os.path.join(current_path, "ui_design", "html_cache", "self_2.html").replace('\\',
                                                                                                          '/') if UserType(
                    self.user_type) == UserType.Student else
                "file:///" + os.path.join(current_path, "ui_design", "html_cache", "all_2.html").replace('\\',
                                                                                                         '/')
            )
            self.chart2.setUrl(self.chart2_url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win_ = Management(201610414206, 1)
    win_.show()
    # win1 = SysHome()
    # win2 = MyInfo()
    # win3 = Register()

    # win4 = Alert()
    #
    # win1.show()
    # win2.show()
    # win3.show()
    # win4.show()
    sys.exit(app.exec_())
