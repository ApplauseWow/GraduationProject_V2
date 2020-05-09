# -*-coding:utf-8-*-
import sys
import time
import datetime
import os
from random import randint

from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QImage
from cv2.cv2 import VideoCapture, resize, cvtColor, COLOR_BGR2RGB, flip, imwrite

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
        self.time_count.timeout.connect(self.close)
        self.time_count.setInterval(800)
        self.time_count.start()


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
        hLayout = QHBoxLayout()

        bt = OperationButtonInTable(name=u'删除')
        bt.clicked.connect(lambda: self.operationOnBtClicked(primary_key))

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
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.show_register = None
        self.show_my_info = self.MyInfo()
        self.show_attendance = self.MyInfo()
        self.show_management = None

        # 设置时间定时器
        self.timer_clock = QTimer()
        self.timer_clock.setInterval(1000)
        self.timer_clock.timeout.connect(self.update_time)
        self.timer_clock.start()

        # 设置摄像头
        self.camera = VideoCapture()  # 摄像头
        self.camera_timer = QTimer()  # 摄像头更新定时器
        self.camera_timer.timeout.connect(self.show_camera)
        self.openCamera()

        # 按钮绑定
        self.quit.clicked.connect(self.close)
        self.open_camera.clicked.connect(self.openOrCloseCamera)
        self.face_login.clicked.connect(self.login)
        self.face_rec.clicked.connect(self.recognize)
        self.face_reg.clicked.connect(self.register)
        self.att_rec.clicked.connect(self.clock_in_or_out)

        # 信号绑定
        # self.show_register.resetCapturePicSignal.connect(self.resetRegisterImageCache)

    def update_time(self):
        """
        更新时间
        :return:None
        """

        self.clock.display(time.strftime("%X", time.localtime()))

    def show_camera(self):
        """
        显示视频
        :return:
        """

        flag, image = self.camera.read()
        if flag:
            image = flip(image, 1)
            show = resize(image, (self.frame.width(), self.frame.height()))
            show = cvtColor(show, COLOR_BGR2RGB)  # opencv读取BGR，pyqt需要RGB
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.frame.setPixmap(QPixmap.fromImage(showImage))
        else:
            self.closeCamera()
            warning = Alert("读取图像失败")
            warning.exec_()

    def openOrCloseCamera(self):
        """
        打开或关闭摄像头
        :return:
        """

        if not self.camera_timer.isActive():  # 已关闭，打开摄像头
            self.openCamera()
        else:  # 已开启，关闭摄像头
            self.closeCamera()

    def openCamera(self):
        """
        打开摄像头
        :return:
        """

        try:
            for device_num in range(3):
                if self.camera.open(device_num):  # 摄像头可用
                    self.camera_timer.start(30)
                    self.open_camera.setText('关闭摄像头')
                    self.clock.raise_()
                    break
            else:  # 摄像头不可用
                raise Exception("no available camera!")
        except Exception as e:
            print(e)
            self.clock.raise_()
            background_img = {0: './ui_design/no_camera1.jpg',
                              1: './ui_design/no_camera2.jpg'}
            self.frame.setPixmap(QPixmap(background_img[randint(0, 1)]))
            warning = Alert("没有可用摄像头")
            warning.exec_()

    def closeCamera(self):
        """
        关闭摄像头
        :return:
        """

        self.camera_timer.stop()  # 停止计时
        self.camera.release()  # 释放摄像头
        self.frame.setPixmap(QPixmap('./ui_design/close_camera.jpg').scaled(self.frame.width(), self.frame.height()))
        self.open_camera.setText('打开摄像头')

    def saveImageCache(self):
        """
        存图片缓存
        :return:
        """

        if self.camera.isOpened():  # 已打开
            flag, image = self.camera.read()
            if flag:
                print(image.shape)
                cache = resize(image, (0, 0), fx=0.35, fy=0.35)
                print(cache.shape[0], cache.shape[1])
                return cache
            else:
                raise Exception('抓拍图像失败')
        else:
            raise Exception('没有可用摄像头')

    def login(self):
        """
        人脸登录
        :return:
        """

        try:
            # 抓拍
            cache = self.saveImageCache()
            # 请求通过人脸识别验证身份
            data = {'image_cache': cache}

            # 创建工作线程
            class Worker(QThread):

                signal = pyqtSignal(dict)
                ui_signal = pyqtSignal(dict)  # 官网建议不要再子线程中处理UI

                def __init__(self, req_data):
                    QThread.__init__(self)
                    self.data = req_data

                def run(self):
                    """
                    耗时工作
                    :return:
                    """
                    try:
                        conn = CR()
                        try:
                            res = conn.CheckIdentityByFaceRequest(self.data)  # 匹配信息，返回姓名、ID、用户类型
                            if res['operation'] == ClientRequest.Success:
                                self.signal.emit(res['result'])
                            else:
                                raise res['exception']
                        except Exception as e:
                            print(e)
                            self.ui_signal.emit({'words': str(e), 'type': None})
                        finally:
                            conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        self.ui_signal.emit({'words': str(e), 'type': None})
                    finally:  # 退出线程，没有exit信号不然会一直守护
                        self.exit()

            def afterEmit(res):
                """
                接收到线程信号后做出响应，主要接收数据
                功能：进入管理系统
                :param res: 数据 -> dict
                :return:
                """

                print(worker.isFinished(), worker.isRunning())
                # 获取身份信息
                self.show_management = Management(user_id=res['user_id'], user_type=res['user_type'])
                self.camera_timer.stop()
                map(lambda x: x.setEnabled(False), self.buttons)  # 进入管理系统后不可操作主界面
                self.show_management.exec_()
                map(lambda x: x.setEnabled(True), self.buttons)
                self.camera_timer.start()

            def showAlert(words_type):
                """
                接收线程信号，主要创建UI
                功能：染出警告窗口
                :param words_type:消息,类型 -> dict
                :return:
                """

                if not words_type['type']:  # 警告窗口
                    window = Alert(words=words_type['words'])
                else:  # 成功窗口
                    window = Alert(words=words_type['words'], _type=words_type['type'])
                window.exec_()

            worker = Worker(data)
            worker.signal.connect(afterEmit)
            worker.ui_signal.connect(showAlert)
            worker.start()
            worker.exec_()  # start后守护，解决卡顿bug
        except Exception as e:
            print(e)
            warning = Alert(str(e))
            warning.exec_()

    def register(self):
        """
        人脸注册
        :return:
        """

        try:
            # 抓拍
            cache = self.saveImageCache()
            # 设置图像
            self.show_register = self.Register()  # 避免迭代exec_()，重新创建
            self.show_register.resetCapturePicSignal.connect(self.resetRegisterImageCache)  # 添加重设图像槽函数
            self.show_register.getImageCache(cache)
            # 显示窗口
            self.show_register.exec_()
        except Exception as e:
            print(e)
            warning = Alert(str(e))
            warning.exec_()

    def resetRegisterImageCache(self):
        """
        重新拍照
        :return:
        """

        try:
            # 抓拍
            cache = self.saveImageCache()
            # 设置
            self.show_register.getImageCache(cache)
        except Exception as e:
            print(e)
            warning = Alert(str(e))
            warning.exec_()

    def recognize(self):
        """
        人脸识别
        :return:
        """

        try:
            # 抓拍
            cache = self.saveImageCache()
            # 请求通过人脸识别验证身份
            data = {'image_cache': cache}

            # 创建工作线程
            class Worker(QThread):

                signal = pyqtSignal(dict)
                ui_signal = pyqtSignal(dict)  # 官网建议不要再子线程中处理UI

                def __init__(self, req_data):
                    QThread.__init__(self)
                    self.data = req_data

                def run(self):
                    """
                    耗时工作
                    :return:
                    """
                    try:
                        conn = CR()
                        try:
                            res = conn.CheckIdentityByFaceRequest(self.data)  # 匹配信息，返回姓名、ID、用户类型
                            if res['operation'] == ClientRequest.Success:
                                self.signal.emit(res['result'])
                            else:
                                raise res['exception']
                        except Exception as e:
                            print(e)
                            self.ui_signal.emit({'words': str(e), 'type': None})
                        finally:
                            conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        self.ui_signal.emit({'words': str(e), 'type': None})
                    finally:  # 退出线程，没有exit信号不然会一直守护
                        self.exit()

            def afterEmit(res):
                """
                接收到线程信号后做出响应，主要接收数据
                功能：显示窗口
                :param res: 数据 -> dict
                :return:
                """

                print(worker.isFinished(), worker.isRunning())
                self.show_my_info.user_name.setText(res['user_name'])
                self.show_my_info.user_type.setText("学生" if UserType(res['user_type']) == UserType.Student else "教师")
                self.show_my_info.user_id.setText(str(res['user_id']))
                self.show_my_info.b_in.hide()
                self.show_my_info.b_off.hide()
                self.show_my_info.b_login.hide()
                # self.show_my_info.b_wrong.hide()
                timer = QTimer()
                timer.timeout.connect(self.show_my_info.close)
                timer.setInterval(3500)
                timer.start()
                self.show_my_info.exec_()

            def showAlert(words_type):
                """
                接收线程信号，主要创建UI
                功能：染出警告窗口
                :param words_type:消息,类型 -> dict
                :return:
                """

                if not words_type['type']:  # 警告窗口
                    window = Alert(words=words_type['words'])
                else:  # 成功窗口
                    window = Alert(words=words_type['words'], _type=words_type['type'])
                window.exec_()

            worker = Worker(data)
            worker.signal.connect(afterEmit)
            worker.ui_signal.connect(showAlert)
            worker.start()
            worker.exec_()  # start后守护，解决卡顿bug
        except Exception as e:
            print(e)
            warning = Alert(str(e))
            warning.exec_()

    def clock_in_or_out(self):
        """
        人脸考勤
        :return:
        """

        try:
            # 抓拍
            cache = self.saveImageCache()
            # 请求通过人脸识别验证身份
            data = {'image_cache': cache}

            # 创建工作线程
            class Worker(QThread):

                signal = pyqtSignal(dict)
                ui_signal = pyqtSignal(dict)  # 官网建议不要再子线程中处理UI

                def __init__(self, req_data):
                    QThread.__init__(self)
                    self.data = req_data

                def run(self):
                    """
                    耗时工作
                    :return:
                    """
                    try:
                        conn = CR()
                        try:
                            res = conn.CheckIdentityByFaceRequest(self.data)  # 匹配信息，返回姓名、ID、用户类型
                            if res['operation'] == ClientRequest.Success:
                                if UserType(res['result']['user_type']) == UserType.Teacher:  # 教师不能考勤
                                    self.ui_signal.emit({'words': "教师无法考勤", 'type': None})
                                else:
                                    self.signal.emit(res['result'])
                            else:
                                raise res['exception']
                        except Exception as e:
                            print(e)
                            self.ui_signal.emit({'words': str(e), 'type': None})
                        finally:
                            conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        self.ui_signal.emit({'words': str(e), 'type': None})
                    finally:  # 退出线程，没有exit信号不然会一直守护
                        self.exit()

            def afterEmit(res):
                """
                接收到线程信号后做出响应，主要接收数据
                功能：显示窗口
                :param res: 数据 -> dict
                :return:
                """

                print(worker.isFinished(), worker.isRunning())
                self.show_attendance.user_name.setText(res['user_name'])
                self.show_attendance.user_type.setText("学生")
                self.show_attendance.user_id.setText(str(res['user_id']))
                self.show_attendance.exec_()

            def showAlert(words_type):
                """
                接收线程信号，主要创建UI
                功能：染出警告窗口
                :param words_type:消息,类型 -> dict
                :return:
                """

                if not words_type['type']:  # 警告窗口
                    window = Alert(words=words_type['words'])
                else:  # 成功窗口
                    window = Alert(words=words_type['words'], _type=words_type['type'])
                window.exec_()

            worker = Worker(data)
            worker.signal.connect(afterEmit)
            worker.ui_signal.connect(showAlert)
            worker.start()
            worker.exec_()  # start后守护，解决卡顿bug
        except Exception as e:
            print(e)
            warning = Alert(str(e))
            warning.exec_()

    class Register(RegisterWindow):
        """
        人脸注册窗口
        """

        resetCapturePicSignal = pyqtSignal()

        def __init__(self):
            RegisterWindow.__init__(self)
            # 待训练样本
            self.training_pic = None

            # 信号绑定
            self.bt_again.clicked.connect(self.resetCapturePicSignal.emit)
            self.bt_cancel.clicked.connect(self.close)
            self.bt_reg.clicked.connect(self.register)

        def getImageCache(self, cache):
            """
            获取图像缓存
            :param cache:
            :return:
            """

            self.training_pic = cache  # 待训练样本
            # 图像处理
            flipped_cache = flip(cache, 1)
            colored_cache = cvtColor(flipped_cache, COLOR_BGR2RGB)  # opencv读取BGR，pyqt需要RGB
            show_cache = QImage(colored_cache.data, colored_cache.shape[1], colored_cache.shape[0],
                                QImage.Format_RGB888)
            self.capture_pic.setPixmap(QPixmap.fromImage(show_cache).scaled(self.capture_pic.width(), self.capture_pic.height()))

        def register(self):
            """
            提交信息注册
            :return:
            """

            if self.checkInput():  # 输入正确
                self.process.show()
                data = {'user_id': int(self.input_id.text()), 'image_cache': self.training_pic}

                class Worker(QThread):

                    signal = pyqtSignal(int)
                    ui_signal = pyqtSignal(dict)  # 处理ui

                    def __init__(self, req_data):
                        QThread.__init__(self)
                        self.data = req_data

                    def run(self):
                        """
                        耗时工作
                        :return:
                        """

                        try:
                            conn = CR()
                            self.signal.emit(26)
                            time.sleep(0.5)
                            try:
                                self.signal.emit(54)
                                res = conn.RegisterRequest(self.data)
                                if res['operation'] == ClientRequest.Success:
                                    self.signal.emit(89)
                                    time.sleep(0.5)
                                    self.signal.emit(100)
                                    self.ui_signal.emit({'words': "注册成功", 'type': 'alright'})
                                else:
                                    raise res['exception']
                            except Exception as e:
                                print(e)
                                self.signal.emit(-1)
                                self.ui_signal.emit({'words': str(e), 'type': None})
                            finally:
                                conn.CloseChannel()
                        except Exception as e:
                            print(e)
                            self.signal.emit(-1)
                            self.ui_signal.emit({'words': str(e), 'type': None})
                        finally:
                            self.exit()

                def afterEmit(response):
                    """
                    线程发出信号，接收数据
                    功能：更新进度条
                    :param response: 进度 -> int
                    :return:
                    """

                    if response == -1:
                        self.resetProcessBar()
                    elif response == 100:
                        self.process.setValue(response)
                        self.close()
                        self.resetProcessBar()
                    else:
                        self.process.setValue(response)

                def showAlert(words_type):
                    """
                    接收线程信号，主要创建UI
                    功能：染出警告窗口
                    :param words_type:消息,类型 -> dict
                    :return:
                    """

                    if not words_type['type']:  # 警告窗口
                        window = Alert(words=words_type['words'])
                    else:  # 成功窗口
                        window = Alert(words=words_type['words'], _type=words_type['type'])
                    window.exec_()

                worker = Worker(data)
                worker.signal.connect(afterEmit)
                worker.ui_signal.connect(showAlert)
                worker.start()
                worker.exec_()

        def resetProcessBar(self):
            """
            重置进度条
            :return:
            """

            self.process.setMinimum(0)
            self.process.setMaximum(100)
            self.process.hide()

        def checkInput(self):
            """
            检查非法输入
            :return:
            """

            szText = self.input_id.text()
            pattern = re.compile('^[0-9]+$')
            match = pattern.match(szText)
            if not match:
                # QMessageBox.information(self, "提示", "请输入数字.")
                msg = Alert(words=u"请输入数字")
                msg.exec_()
                return False
            if szText == "":
                # QMessageBox.information(self, "提示", "请输入跳转页面.")
                msg = Alert(words=u"ID为空")
                msg.exec_()
                return False
            return True

        def closeEvent(self, QCloseEvent):
            """
            关闭窗口时
            :param QCloseEvent:
            :return:
            """

            self.input_id.clear()
            self.resetProcessBar()

        def keyPressEvent(self, QKeyEvent):
            """
            按esc关闭窗口
            :param QKeyEvent:
            :return:
            """

            if QKeyEvent.key() == Qt.Key_Escape:  # clicked the ESC
                self.close()

    class MyInfo(InfoWindow):
        """
        考勤窗口｜个人信息显示窗口
        """

        def __init__(self):
            InfoWindow.__init__(self)
            # 按钮绑定槽函数
            self.b_in.clicked.connect(lambda: self.clock_in_or_out(AttendanceType.ClockIn.value))
            self.b_off.clicked.connect(lambda: self.clock_in_or_out(AttendanceType.ClockOut.value))
            self.b_wrong.clicked.connect(self.tryToRegisterAgain)
            self.b_login.clicked.connect(self.close)

        def clock_in_or_out(self, _type):
            """
            学生考勤打卡
            :param _type:考勤类型
            :return:
            """

            t = time.localtime(time.time())
            data = {
                'user_id': int(self.user_id.text()),
                'date_time': datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday,
                                               t.tm_hour, t.tm_min, t.tm_sec),
                'record_type': _type
            }
            try:
                conn = CR()
                try:
                    res = conn.ClockInOrOutRequest(data)
                    if res['operation'] == ClientRequest.Success:
                        self.close()
                        alright = Alert(words="考勤成功", _type='alright')
                        alright.exec_()
                    else:
                        raise res['exception']
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()
            except Exception as e:
                print(e)
                warning = Alert(str(e))
                warning.exec_()

        def tryToRegisterAgain(self):
            """
            身份识别有误，提示重新注册
            :return:
            """

            warning = Alert(words="重试或重新注册")
            warning.exec_()

        def closeEvent(self, QCloseEvent):
            """
            关闭窗口时
            :param QCloseEvent:
            :return:
            """

            self.user_id.clear()
            self.user_type.clear()
            self.user_name.clear()

        def keyPressEvent(self, QKeyEvent):
            """
            按esc关闭窗口
            :param QKeyEvent:
            :return:
            """

            if QKeyEvent.key() == Qt.Key_Escape:  # clicked the ESC
                self.close()


class Management(ManagementWindow):
    """
    资源管理窗口
    """

    def __init__(self, user_id, user_type):
        ManagementWindow.__init__(self, user_id, user_type)
        try:
            # 检查与服务端连接状态
            check_connection = CR()
            del check_connection
            # 添加顺序一定按照按钮顺序
            self.page_one = self.ShowUsers(user_id=user_id, user_type=user_type) if UserType(
                user_type) == UserType.Teacher else self.ShowMyself(user_id=user_id, user_type=user_type)
            self.page_two = self.ShowNotes(user_id=user_id, user_type=user_type)
            self.page_three = self.ShowAttendanceCharts(user_id=user_id, user_type=user_type)
            self.page_four = self.ShowGroups(user_id=user_id, user_type=user_type) if UserType(
                user_type) == UserType.Teacher else self.ShowMyGroup(user_id=user_id, user_type=user_type)
            self.page_five = self.ShowProjects(user_id=user_id, user_type=user_type)
            self.page_six = self.ShowCompetitions(user_id=user_id, user_type=user_type)
            self.page_seven = self.ShowAchievements(user_id=user_id, user_type=user_type)
            self.page_eight = self.ShowPermits(user_id=user_id, user_type=user_type)
            self.page_nine = self.ShowSources(user_id=user_id, user_type=user_type)
            self.page_ten = self.ShowTasks(user_id=user_id, user_type=user_type)
            self.page_eleven = self.ShowSeats(user_id=user_id, user_type=user_type)

            self.right_layout.addWidget(self.page_one)
            self.right_layout.addWidget(self.page_two)
            self.right_layout.addWidget(self.page_three)
            self.right_layout.addWidget(self.page_four)
            self.right_layout.addWidget(self.page_five)
            self.right_layout.addWidget(self.page_six)
            self.right_layout.addWidget(self.page_seven)
            self.right_layout.addWidget(self.page_eight)
            self.right_layout.addWidget(self.page_nine)
            self.right_layout.addWidget(self.page_ten)
            self.right_layout.addWidget(self.page_eleven)
        except Exception as e:
            print(e)
            warning = Alert(str(e))
            warning.exec_()

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
            self.setEnabled(False)
            index = self.menu_dict[self.sender().objectName()]
            if index != self.menu_dict['exit']:
                self.right_layout.setCurrentIndex(index)
                self.right_layout.widget(index).initPage()  # 所有组内控件重写一个初始化函数解决了堆叠控件切换后刷新问题
            else:  # 退出按钮
                self.close()
        except Exception as e:
            print(e)
            warning = Alert(words=u"切换失败！")
            warning.exec_()
        finally:
            self.setEnabled(True)

    def keyPressEvent(self, QKeyEvent):
        """
        按esc关闭窗口
        :param QKeyEvent:
        :return:
        """

        if QKeyEvent.key() == Qt.Key_Escape:  # clicked the ESC
            self.close()

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
                    try:
                        self.currentPage = 1
                        self.totalRecordCount = conn.GetCountRequest('note', {'is_valid': NoteStatus.Valid.value})
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
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

            def queryRecord(self, limit_index):
                """
                重写查询记录
                :param limit_index:从第limitIndex条开始
                :return:
                """

                try:
                    conn = CR()
                    try:
                        notes = conn.GetAllNotesRequest(start=limit_index, num=self.pageRecordCount,
                                                        is_valid=NoteStatus.Valid.value)
                        self.addRecords(self.col_list, notes)
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"查询失败！")
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

            def operationOnBtClicked(self, primary_key):
                """
                重写操作按钮
                :param primary_key: 主键
                :return: None
                """

                try:
                    conn = CR()
                    try:
                        # 更新
                        res = conn.VoidTheNoteRequest(primary_key)
                        if res == ClientRequest.Success:
                            alright = Alert(words=u"操作成功！", _type='alright')
                            alright.exec_()
                            self.update_signal.emit()  # 更新页面
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"操作失败！")
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
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
                    try:
                        self.currentPage = 1
                        self.totalRecordCount = conn.GetCountRequest('note', {'is_valid': NoteStatus.Invalid.value})
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
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

            def queryRecord(self, limitIndex):
                """
                重写查询记录
                :param limitIndex:从第limitIndex条开始
                :return:
                """

                try:
                    conn = CR()
                    try:
                        notes = conn.GetAllNotesRequest(start=limitIndex, num=self.pageRecordCount,
                                                        is_valid=NoteStatus.Invalid.value)
                        self.addRecords(self.col_list, notes)
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"查询失败！")
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
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
                    try:
                        res = conn.InsertANoteRequest(data)
                        if res == ClientRequest.Success:
                            self.close()
                            alright = Alert(words=u"操作成功！", _type='alright')
                            alright.exec_()
                            self.update_signal.emit()
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"操作失败！")
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

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
                    try:
                        res = conn.ModifyTheNoteRequest(data)
                        if res == ClientRequest.Success:
                            self.close()
                            alright = Alert(words=u"操作成功！", _type='alright')
                            alright.exec_()
                            self.update_signal.emit()
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"操作失败！")
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

    # ---------------------ShowNote  complete------------------------

    class ShowUsers(StuffTable):
        """
        继承StuffTable封装业务逻辑
        数据需求：所有用户信息
        描述：【教师】一个用户表格
        """

        def __init__(self, user_id, user_type):
            StuffTable.__init__(self)
            self.user_table = self.UserTable(user_type, user_id)
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

            def __init__(self, user_type, user_id):
                Page.__init__(self)
                self.user_type = user_type
                self.user_id = user_id
                self.col_list = TABLE_COLUMN_DICT[UserType(user_type)]['user']  # 获取表头信息
                self.initializedModel()
                self.setUpConnect()
                self.updateStatus()

            def initializedModel(self):
                try:
                    conn = CR()
                    try:
                        self.currentPage = 1
                        self.totalRecordCount = conn.GetCountRequest('user')
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
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

            def queryRecord(self, limitIndex):
                """
                重写查询记录
                :param limitIndex:从第limitIndex条开始
                :return:
                """

                try:
                    conn = CR()
                    try:
                        users = conn.GetAllUserRequest(start=limitIndex, num=self.pageRecordCount)
                        self.addRecords(self.col_list, users)
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"查询失败！")
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

            def operationOnBtClicked(self, primary_key):
                """
                重写操作按钮
                :param primary_key: 主键
                :return: None
                """

                try:
                    if primary_key[0] == self.user_id:
                        raise Exception("禁止删除本人")
                    elif primary_key[0] == 201610414202:
                        raise Exception("禁止删除此用户")
                    else:
                        pass
                    conn = CR()
                    try:
                        # 更新
                        res = conn.DeleteTheUserRequest(primary_key)
                        if res == ClientRequest.Success:
                            alright = Alert(words=u"操作成功！", _type='alright')
                            alright.exec_()
                            self.initializedModel()  # 重新刷新页面色
                            self.updateStatus()
                            self.update_signal.emit()
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"操作失败！")
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
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
                    self.d_user_name.setText(data['user_name'])
                    self.d_major.setText(data['major'])
                    self.d_user_type.setCurrentIndex(data['user_type'])
                    self.d_grade.setText(data['grade'])
                    self.d_class.setText(data['_class'])
                    self.d_tel.setText(data['tel'])
                    self.d_email.setText(data['email'])
                    self.isTeacher(None)
                    if UserType(int(data['user_type'])) == UserType.Student:
                        self.initCharts(int(data['user_id']))
                    else:
                        self.timestamp.hide()
                        self.hour_everyday.hide()

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
                    try:
                        res_everyday_hour = conn.GetWorkHourEveryDayRequest(data)
                        res_timestamp = conn.GetClockInOrOutTimeStampRequest(data)
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
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

            def CreateNewUser(self):
                """
                创建新公告
                :return: None
                """

                if self.checkInput():
                    data = {
                        'user_id': int(self.d_user_id.text()),
                        'user_name': self.d_user_name.text(),
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
                        try:
                            res = conn.InsertAUserRequest(data)
                            if res == ClientRequest.Success:
                                self.close()
                                alright = Alert(words=u"操作成功！", _type='alright')
                                alright.exec_()
                                self.update_signal.emit()
                        except Exception as e:
                            print(e)
                            warning = Alert(words=u"操作失败！")
                            warning.exec_()
                        finally:
                            conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        warning = Alert(str(e))
                        warning.exec_()

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
                        'user_name': self.d_user_name.text(),
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
                        try:
                            res = conn.ModifyTheUserRequest(data)
                            if res == ClientRequest.Success:
                                self.close()
                                alright = Alert(words=u"操作成功！", _type='alright')
                                alright.exec_()
                                self.update_signal.emit()
                        except Exception as e:
                            print(e)
                            warning = Alert(words=u"操作失败！")
                            warning.exec_()
                        finally:
                            conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        warning = Alert(str(e))
                        warning.exec_()

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

                checks = [self.d_user_id, self.d_user_name,
                          self.d_grade, self.d_major,
                          self.d_class, self.d_tel, self.d_email] if UserType(self.d_user_type.currentData()) == UserType.Student else [self.d_user_id, self.d_tel, self.d_email]
                for sz in checks:
                    szText = sz.text()
                    if sz is self.d_major or sz is self.d_email or sz is self.d_user_name:
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
                try:
                    data = {'user_id': self.user_id}
                    Col2Index = ColName2Index['user']
                    data = conn.GetSelfInfoRequest(data)
                    self.d_user_id.setText(str(data[Col2Index['user_id']]))
                    self.d_user_name.setText(data[Col2Index['user_name']])
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
                finally:
                    conn.CloseChannel()
            except Exception as e:
                print(e)
                warning = Alert(str(e))
                warning.exec_()

        def ModifySelfInfo(self):
            """
            修改个人信息
            :return: None
            """

            if self.checkInput():
                try:
                    mapper = {u"教师": UserType.Teacher.value, u"学生": UserType.Student.value}
                    data = {
                        'user_id': int(self.d_user_id.text()),
                        'user_name': self.d_user_name.text(),
                        'user_type': mapper[self.d_user_type.text()],
                        'major': self.d_major.text(),
                        'grade': int(self.d_grade.text()),
                        '_class': int(self.d_class.text()),
                        'tel': int(self.d_tel.text()),
                        'email': self.d_email.text()
                    }
                    conn = CR()
                    try:
                        res = conn.ModifyTheUserRequest(data)
                        if res == ClientRequest.Success:
                            alright = Alert(words=u"操作成功！", _type='alright')
                            alright.exec_()
                            self.update_signal.emit()
                    except Exception as e:
                        print(e)
                        warning = Alert(words=u"操作失败！")
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
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
            self.initPage()

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            self.initCharts()

        def initCharts(self):
            """
            创建图表页面
            :return:
            """

            try:
                # 查询数据，此处应该更优雅，时间来不及，不值得执着于优美代码
                conn = CR()
                try:
                    if UserType(self.user_type) == UserType.Student:  # 学生个人考勤页面
                        data = {'user_id': self.user_id}
                        res_everyday_hour = conn.GetWorkHourEveryDayRequest(data)
                        res_timestamp = conn.GetClockInOrOutTimeStampRequest(data)
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
                    else:  # 全体考勤页面
                        data = {}
                        res_location = conn.GetClockInOrOutCountEachHourRequest(data)
                        res_clockin_today = conn.GetClockInRateTodayRequest(data)
                        # 创建js文件
                        with open('./ui_design/js/html_model.html', 'r') as f:
                            html_head = f.read()
                        with open('./ui_design/js/aweek_every_hour_clockIn.js', 'r') as f:
                            js_each_hour = f.read()
                        with open('./ui_design/js/today_clockIn_rate.js', 'r') as f:
                            js_today_rate = f.read()
                        html_clock_in = "".join([html_head.format(800, 400),
                                                 "<script>var data = {};var label = '{}';</script>".format(
                                                     res_location['clock_in'], '到岗人数'),
                                                 "<script>",
                                                 js_each_hour,
                                                 "</script></body></html>"])
                        html_clock_out = "".join([html_head.format(800, 400),
                                                  "<script>var data = {};var label = '{}'</script>".format(
                                                      res_location['clock_out'], '离岗人数'),
                                                  "<script>",
                                                  js_each_hour,
                                                  "</script></body></html>"])
                        html_clock_in_rate = "".join([html_head.format(400, 400),
                                                      "<script type='text/javascript' src='../js/echarts-liquidfill.js'></script>",
                                                      "<script>var clock_in = {};var total = {};</script>".format(
                                                          res_clockin_today['clock_in'], res_clockin_today['total']),
                                                      "<script>",
                                                      js_today_rate,
                                                      "</script></body></html>"])
                        with open('./ui_design/html_cache/all_1.html', 'w') as f:
                            f.write(html_clock_in)
                        with open('./ui_design/html_cache/all_2.html', 'w') as f:
                            f.write(html_clock_out)
                        with open('./ui_design/html_cache/all_3.html', 'w') as f:
                            f.write(html_clock_in_rate)

                    current_path = os.getcwd()  # 当前目录
                    # 加载网页
                    if UserType(self.user_type) == UserType.Teacher:
                        self.chart1_url.setUrl("file:///" + os.path.join(current_path, "ui_design", "html_cache", "all_3.html").replace('\\', '/'))
                        self.chart1.setUrl(self.chart1_url)
                        self.chart2_url.setUrl("file:///" + os.path.join(current_path, "ui_design", "html_cache", "all_1.html").replace('\\', '/'))
                        self.chart2.setUrl(self.chart2_url)
                        self.chart3_url.setUrl("file:///" + os.path.join(current_path, "ui_design", "html_cache", "all_2.html").replace('\\', '/'))
                        self.chart3.setUrl(self.chart3_url)
                    else:
                        self.chart1_url.setUrl(
                            "file:///" + os.path.join(current_path, "ui_design", "html_cache", "self_1.html").replace('\\', '/'))
                        self.chart1.setUrl(self.chart1_url)
                        self.chart2_url.setUrl(
                            "file:///" + os.path.join(current_path, "ui_design", "html_cache", "self_2.html").replace('\\', '/'))
                        self.chart2.setUrl(self.chart2_url)
                except Exception as e:
                    print(e)
                    warning = Alert(words=u" 统计失败！")
                    warning.exec_()
                finally:
                    conn.CloseChannel()
            except Exception as e:
                print(e)
                warning = Alert(str(e))
                warning.exec_()

    # ---------------------ShowAttendanceCharts  complete------------------------

    class ShowGroups(GroupTable):

        def __init__(self, user_id, user_type):
            GroupTable.__init__(self)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

        class AGroup(GroupDetail):

            def __init__(self):
                GroupDetail.__init__(self)

    # ---------------------ShowGroups  complete----------------------------------

    class ShowMyGroup(MyGroup):

        def __init__(self, user_id, user_type):
            MyGroup.__init__(self)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

    # ---------------------ShowMyGroup  complete----------------------------------

    class ShowSources(SourceTable):

        def __init__(self, user_id, user_type):
            SourceTable.__init__(self)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

        class ASource(SourceDetail):

            def __init__(self):
                SourceDetail.__init__(self)

    # ---------------------ShowSources  complete----------------------------------

    class ShowPermits(PermitTable):

        def __init__(self, user_id, user_type):
            PermitTable.__init__(self)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

        class APermit(PermitDetail):

            def __init__(self):
                PermitDetail.__init__(self)

    # ---------------------ShowPermits  complete----------------------------------

    class ShowAchievements(AchievementTable):

        def __init__(self, user_id, user_type):
            AchievementTable.__init__(self)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

        class AAchievement(AchievementDetail):

            def __init__(self):
                AchievementDetail.__init__(self)

    # ---------------------ShowAchievements  complete----------------------------

    class ShowCompetitions(CompetitionTable):

        def __init__(self, user_id, user_type):
            CompetitionTable.__init__(self)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

        class ACompetition(CompetitionDetail):

            def __init__(self):
                CompetitionDetail.__init__(self)

    # ---------------------ShowCompetitions  complete---------------------------

    class ShowProjects(ProjectTable):

        def __init__(self, user_id, user_type):
            ProjectTable.__init__(self)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

        class AProject(ProjectDetail):

            def __init__(self):
                ProjectDetail.__init__(self)

    # ---------------------ShowProjects  complete----------------------------------

    class ShowTasks(TaskArrangement):

        def __init__(self, user_id, user_type):
            TaskArrangement.__init__(self)

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            pass

        class ATask(TaskDetail):

            def __init__(self):
                TaskDetail.__init__(self)

    # ---------------------ShowTasks  complete-------------------------------------

    class ShowSeats(SeatLocation):
        """
        工位部署情况
        """

        def __init__(self, user_id, user_type):
            SeatLocation.__init__(self)
            self.user_type = user_type
            self.user_id = user_id
            if UserType(self.user_type) == UserType.Student:
                self.bt_deploy_seats.hide()
                self.d_deploy_col.setEnabled(False)
                self.d_deploy_row.setEnabled(False)
            else:
                pass

            self.bt_deploy_seats.clicked.connect(self.deploySeats)
            # self.initPage()

        def initPage(self):
            """
            用于切换页面后的初始化页面，仅初始化必要控件
            :return: None
            """

            try:
                conn = CR()
                try:
                    res = conn.GetSeatsDeploymentRequest()
                    if res['operation'] == ClientRequest.Success:
                        if len(res['result']) == 0:  # 没有部署
                            raise Exception("暂未部署工位")
                        else:  # 生成部署图
                            # 获取安排
                            res_arrangement = conn.GetSeatsArrangementRequest()
                            if res_arrangement['operation'] == ClientRequest.Success:
                                arrangements = res_arrangement['result']  # 获取部署安排
                            else:
                                warning = Alert(words="获取安排失败")
                                warning.exec_()
                                arrangements = None
                            # 部署
                            for num in range(self.seat_deploy_layout.count()):
                                self.seat_deploy_layout.itemAt(num).widget().deleteLater()
                            for seat in res['result']:
                                seat_id = seat[ColName2Index['seat']['seat_id']]  # 工位id
                                # 工位坐标
                                row = seat[ColName2Index['seat']['row']]
                                col = seat[ColName2Index['seat']['col']]
                                bt_seat = self.createASeat(seat_id, row, col)
                                self.seat_deploy_layout.addWidget(bt_seat, row-1, col-1, 1, 1)
                                if arrangements:  # 有安排信息
                                    checks = filter(
                                        lambda arrangement: True if seat[ColName2Index['seat']['seat_id']] == arrangement[
                                            ColName2Index['seat_arrangement']['seat_id']] else False, arrangements)
                                    if checks:  # 工位有人
                                        mine = filter(lambda check: True if self.user_id == check[
                                            ColName2Index['seat_arrangement']['user_id']] else False, checks)
                                        if mine:  # 个人工位
                                            bt_seat.setObjectName("my_seat")
                                        else:  # 非个人工位
                                            bt_seat.setObjectName("exist_user")
                                    else:  # 工位没人
                                        bt_seat.setObjectName("no_user")
                                else:  # 没安排
                                    bt_seat.setObjectName("no_user")
                            else:
                                self.d_deploy_row.setText(str(res['result'][-1][ColName2Index['seat']['row']]))
                                self.d_deploy_col.setText(str(res['result'][-1][ColName2Index['seat']['col']]))
                    else:
                        raise Exception("获取部署失败")
                except Exception as e:
                    print(e)
                    warning = Alert(words=str(e))
                    warning.exec_()
                finally:
                    conn.CloseChannel()
            except Exception as e:
                print(e)
                warning = Alert(str(e))
                warning.exec_()

        def createASeat(self, seat_id, row, col):
            """
            生成一个工位(按钮)
            :param seat_id:工位id
            :param row: 行
            :param col: 列
            :return:
            """

            bt_seat = QPushButton()
            bt_seat.setFixedSize(100, 50)
            bt_seat.setText("{}行{}列".format(row, col))
            bt_seat.clicked.connect(lambda: self.showTheSeat(seat_id))  # 传递seat_id
            return bt_seat

        def deploySeats(self):
            """
            部署工位
            :return:
            """

            if self.checkInput():
                data = {'row': int(self.d_deploy_row.text()), 'col': int(self.d_deploy_col.text())}
                try:
                    conn = CR()
                    try:
                        res = conn.DeploySeatsRequest(data)
                        if res['operation'] == ClientRequest.Success:
                            alright = Alert(words="部署成功", _type='alright')
                            alright.exec_()
                            self.initPage()
                        else:
                            raise Exception("部署失败")
                    except Exception as e:
                        print(e)
                        warning = Alert(words=str(e))
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

        def showTheSeat(self, seat_id):
            """
            工位详情
            :param sender: 所点击的按钮
            :param seat_id: 工位id
            :return:
            """

            seat = self.ASeat(user_type=self.user_type, seat_id=seat_id)
            seat.update_signal.connect(self.initPage)  # 更新部署图
            seat.exec_()

        def checkInput(self):
            """
            检查非法输入
            :return:
            """

            checks = [self.d_deploy_row, self.d_deploy_col]
            for sz in checks:
                szText = sz.text()
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

        class ASeat(SeatDetail):
            """
            工位详情
            """

            update_signal = pyqtSignal()  # 更新工位部署图

            def __init__(self, user_type, seat_id):
                SeatDetail.__init__(self)
                self.seat_id = seat_id
                self.arrangement_table = self.ArrangementTable(user_type=user_type, seat_id=self.seat_id)
                self.user_table_layout.addWidget(self.arrangement_table)
                if UserType(user_type) == UserType.Student:
                    self.bt_arrangement.hide()
                    self.d_user_name.hide()
                    self.l_user.hide()
                    self.d_is_leader.hide()
                else:
                    self.initUserComboBox()

                # 绑定信号槽函数
                self.arrangement_table.update_signal.connect(self.update_signal.emit)
                self.bt_arrangement.clicked.connect(self.arrangeStudent)
                self.quit.clicked.connect(self.close)

            def initUserComboBox(self):
                """
                初始化学生下拉框
                :return:
                """

                try:
                    conn = CR()
                    try:
                        data = {'user_type': UserType.Student.value}
                        res = conn.GetAllStudentsRequest(data)  # 获取所有学生名单
                        if res['operation'] == ClientRequest.Success:
                            # 生成下拉列表
                            for stu in res['result']:
                                self.d_user_name.addItem(stu[ColName2Index['user']['user_name']], stu[ColName2Index['user']['user_id']])
                            self.d_user_name.setCurrentIndex(-1)
                        else:
                            raise Exception("获取学生失败")
                    except Exception as e:
                        print(e)
                        warning = Alert(words=str(e))
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

            def arrangeStudent(self):
                """
                给学生安排工位
                :return:
                """

                try:
                    conn = CR()
                    try:
                        data = {'user_id': self.d_user_name.currentData(), 'seat_id': self.seat_id, 'is_leader': self.d_is_leader.currentData()}
                        res = conn.ArrangeTheStudentHereRequest(data)  # 获取所有学生名单
                        if res['operation'] == ClientRequest.Success:
                            alright = Alert(words=u"安排成功", _type='alright')
                            alright.exec_()
                            self.arrangement_table.initializedModel()  # 重新刷新页面
                            self.arrangement_table.updateStatus()
                            self.update_signal.emit()
                        else:
                            raise Exception("安排失败")
                    except Exception as e:
                        print(e)
                        warning = Alert(words=str(e))
                        warning.exec_()
                    finally:
                        conn.CloseChannel()
                except Exception as e:
                    print(e)
                    warning = Alert(str(e))
                    warning.exec_()

            class ArrangementTable(Page):
                """
                安排表
                """

                update_signal = pyqtSignal()

                def __init__(self, user_type, seat_id):
                    Page.__init__(self)
                    self.user_type = user_type
                    self.seat_id = seat_id
                    self.col_list = TABLE_COLUMN_DICT[UserType(user_type)]['seat_arrangement']  # 获取表头信息
                    self.initializedModel()
                    self.setUpConnect()
                    self.updateStatus()

                def initializedModel(self):
                    try:
                        conn = CR()
                        try:
                            # 初始化表格
                            data = {'seat_id': self.seat_id}
                            res = conn.GetTheSeatArrangementRequest(data)
                            if res['operation'] == ClientRequest.Success:
                                # 显示数据
                                self.currentPage = 1
                                self.totalRecordCount = len(res['result'])
                                if self.totalRecordCount % self.pageRecordCount == 0:
                                    if self.totalRecordCount != 0:
                                        self.totalPage = self.totalRecordCount / self.pageRecordCount
                                    else:
                                        self.totalPage = 1
                                else:
                                    self.totalPage = int(self.totalRecordCount / self.pageRecordCount) + 1
                                self.queryRecord(0)
                            else:
                                raise Exception("获取安排信息失败")
                        except Exception as e:
                            print(e)
                            warning = Alert(words=str(e))
                            warning.exec_()
                        finally:
                            conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        warning = Alert(str(e))
                        warning.exec_()

                def queryRecord(self, limitIndex):
                    """
                    重写查询记录
                    :param limitIndex:从第limitIndex条开始
                    :return:
                    """

                    try:
                        conn = CR()
                        try:
                            data = {'seat_id': self.seat_id, 'start': limitIndex, 'num': self.pageRecordCount}
                            res = conn.GetTheSeatArrangementRequest(data)
                            if res['operation'] == ClientRequest.Success:
                                users = res['result']
                                self.addRecords(self.col_list, users)
                            else:
                                raise Exception("获取安排信息失败")
                        except Exception as e:
                            print(e)
                            warning = Alert(words=str(e))
                            warning.exec_()
                        finally:
                            conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        warning = Alert(str(e))
                        warning.exec_()

                def operationOnBtClicked(self, primary_key):
                    """
                    重写操作按钮
                    :param primary_key: 主键
                    :return: None
                    """

                    try:
                        conn = CR()
                        try:
                            # 更新
                            res = conn.DeleteTheArrangementRequest(primary_key)
                            if res['operation'] == ClientRequest.Success:
                                alright = Alert(words=u"操作成功！", _type='alright')
                                alright.exec_()
                                self.initializedModel()  # 重新刷新页面
                                self.updateStatus()
                                self.update_signal.emit()
                            else:
                                raise res['exception']
                        except Exception as e:
                            print(e)
                            warning = Alert(str(e))
                            warning.exec_()
                        finally:
                            conn.CloseChannel()
                    except Exception as e:
                        print(e)
                        warning = Alert(str(e))
                        warning.exec_()

    # ---------------------ShowSeats  complete--------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win_ = Management(201610414206, 1)
    win_.show()

    # win2 = MyInfo()
    # win3 = SysHome().Register()

    # win4 = Alert()

    # win1 = SysHome()
    # win1.show()

    # win2.show()
    # win3.show()
    # win4.show()
    sys.exit(app.exec_())
