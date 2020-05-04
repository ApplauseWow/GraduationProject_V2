# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_win.ui'
#
# Created: Sun May  3 16:32:46 2020
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(882, 695)
        MainWindow.setMaximumSize(QtCore.QSize(882, 695))
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.centralwidget.setObjectName("centralwidget")
        self.face_login = QtWidgets.QPushButton(self.centralwidget)
        self.face_login.setGeometry(QtCore.QRect(610, 440, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.face_login.setFont(font)

        self.face_login.setObjectName("face_login")
        self.att_rec = QtWidgets.QPushButton(self.centralwidget)
        self.att_rec.setGeometry(QtCore.QRect(610, 385, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.att_rec.setFont(font)

        self.att_rec.setObjectName("att_rec")
        self.face_reg = QtWidgets.QPushButton(self.centralwidget)
        self.face_reg.setGeometry(QtCore.QRect(610, 275, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.face_reg.setFont(font)

        self.face_reg.setObjectName("face_reg")
        self.face_rec = QtWidgets.QPushButton(self.centralwidget)
        self.face_rec.setGeometry(QtCore.QRect(610, 330, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.face_rec.setFont(font)

        self.face_rec.setObjectName("face_rec")
        self.clock = QtWidgets.QLCDNumber(self.centralwidget)
        self.clock.setGeometry(QtCore.QRect(70, 580, 64, 23))
        self.clock.setObjectName("clock")
        self.frame = QtWidgets.QLabel(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 0, 851, 681))
        self.frame.setText("")
        self.frame.setObjectName("frame")
        self.quit = QtWidgets.QPushButton(self.centralwidget)
        self.quit.setGeometry(QtCore.QRect(610, 490, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.quit.setFont(font)

        self.quit.setObjectName("quit")
        self.open_camera = QtWidgets.QPushButton(self.centralwidget)
        self.open_camera.setGeometry(QtCore.QRect(610, 220, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.open_camera.setFont(font)

        self.open_camera.setObjectName("open_camera")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.face_login.setText(_translate("MainWindow", "登录系统"))
        self.att_rec.setText(_translate("MainWindow", "考勤打卡"))
        self.face_reg.setText(_translate("MainWindow", "人脸注册"))
        self.face_rec.setText(_translate("MainWindow", "人脸识别"))
        self.quit.setText(_translate("MainWindow", "退出系统"))
        self.open_camera.setText(_translate("MainWindow", "打开摄像头"))
