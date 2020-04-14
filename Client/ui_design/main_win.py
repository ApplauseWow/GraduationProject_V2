# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_win.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
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
        self.face_login.setStyleSheet("QPushButton{"
"                   background-color:rgba(255,165,0,30);"
"                   border-style:outset;                  "
"                   border-width:4px;                     "
"                   border-radius:10px;                "
"                   border-color:rgba(255,255,255,30);   "
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
"                   }")
        self.face_login.setObjectName("face_login")
        self.att_rec = QtWidgets.QPushButton(self.centralwidget)
        self.att_rec.setGeometry(QtCore.QRect(610, 385, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.att_rec.setFont(font)
        self.att_rec.setStyleSheet("QPushButton{"
"                   background-color:rgba(255,165,0,30);"
"                   border-style:outset;                  "
"                   border-width:4px;                     "
"                   border-radius:10px;                "
"                   border-color:rgba(255,255,255,30);   "
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
"                   }")
        self.att_rec.setObjectName("att_rec")
        self.face_reg = QtWidgets.QPushButton(self.centralwidget)
        self.face_reg.setGeometry(QtCore.QRect(610, 275, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.face_reg.setFont(font)
        self.face_reg.setStyleSheet("QPushButton{"
"                   background-color:rgba(255,165,0,30);"
"                   border-style:outset;                  "
"                   border-width:4px;                     "
"                   border-radius:10px;                "
"                   border-color:rgba(255,255,255,30);   "
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
"                   }")
        self.face_reg.setObjectName("face_reg")
        self.face_rec = QtWidgets.QPushButton(self.centralwidget)
        self.face_rec.setGeometry(QtCore.QRect(610, 330, 199, 46))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.face_rec.setFont(font)
        self.face_rec.setStyleSheet("QPushButton{"
"                   background-color:rgba(255,165,0,30);"
"                   border-style:outset;                  "
"                   border-width:4px;                     "
"                   border-radius:10px;                "
"                   border-color:rgba(255,255,255,30);   "
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
"                   }")
        self.face_rec.setObjectName("face_rec")
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

