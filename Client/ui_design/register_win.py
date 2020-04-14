# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register_win.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_register_win(object):
    def setupUi(self, register_win):
        register_win.setObjectName("register_win")
        register_win.resize(431, 334)
        self.bt_reg = QtWidgets.QPushButton(register_win)
        self.bt_reg.setGeometry(QtCore.QRect(290, 60, 121, 41))
        self.bt_reg.setObjectName("bt_reg")
        self.bt_again = QtWidgets.QPushButton(register_win)
        self.bt_again.setGeometry(QtCore.QRect(290, 120, 121, 41))
        self.bt_again.setObjectName("bt_again")
        self.bt_cancel = QtWidgets.QPushButton(register_win)
        self.bt_cancel.setGeometry(QtCore.QRect(290, 180, 121, 41))
        self.bt_cancel.setObjectName("bt_cancel")
        self.capture_pic = QtWidgets.QLabel(register_win)
        self.capture_pic.setGeometry(QtCore.QRect(50, 50, 201, 121))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.capture_pic.sizePolicy().hasHeightForWidth())
        self.capture_pic.setSizePolicy(sizePolicy)
        self.capture_pic.setObjectName("capture_pic")
        self.formLayoutWidget = QtWidgets.QWidget(register_win)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 190, 221, 62))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setObjectName("formLayout")
        self.Label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Label.setFont(font)
        self.Label.setObjectName("Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.input_id = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.input_id.setObjectName("input_id")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_id)
        self.process = QtWidgets.QProgressBar(self.formLayoutWidget)
        self.process.setProperty("value", 24)
        self.process.setObjectName("process")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.process)

        self.retranslateUi(register_win)
        QtCore.QMetaObject.connectSlotsByName(register_win)

    def retranslateUi(self, register_win):
        _translate = QtCore.QCoreApplication.translate
        register_win.setWindowTitle(_translate("register_win", "Dialog"))
        self.bt_reg.setText(_translate("register_win", "确定注册"))
        self.bt_again.setText(_translate("register_win", "重新拍照"))
        self.bt_cancel.setText(_translate("register_win", "取消注册"))
        self.capture_pic.setText(_translate("register_win", "照片"))
        self.Label.setText(_translate("register_win", "工号/学号"))

