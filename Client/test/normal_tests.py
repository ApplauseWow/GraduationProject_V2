# -*-coding:utf-8-*-
# 用于各种小测试
import sys

from PyQt5.QtWidgets import QApplication

from TypesEnum import *


if __name__ == '__main__':
    # from PyQt5.QtWebKitWidgets import QWebView
    # from PyQt5 import QtCore
    # from pyecharts import Bar
    #
    # bar = Bar('第一个图', '直方图')
    # kwargs = dict(
    #     name='柱形图',
    #     x_axis=['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
    #     y_axis=[5, 20, 36, 10, 75, 90]
    #     # bar_category_gap = 0 间距
    # )
    # bar.add(**kwargs)
    # bar.render()
    #
    # app = QApplication(sys.argv)
    # win_ = QWebView()
    # win_.load(QtCore.QUrl('file:///D:/Bingo/AI_WorkPlace/GraduationProject/GraduationProject/Client/test/render.html'))
    # win_.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 影藏窗口
    # win_.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)  # 取消滚动条
    # win_.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
    # win_.resize(300, 400)
    # win_.show()
    # sys.exit(app.exec_())
    from cv2.cv2 import imread
    import dlib
    from face_recognition import face_locations, face_encodings

    detector = dlib.get_frontal_face_detector()
    img = imread('1.jpg')
    dets = detector(img, 1)
    print(dets, len(dets))
    face_location = face_locations(img, model='cnn')
    _face_location = [].append(face_location[0])
    print dlib.DLIB_USE_CUDA
    face_encoding = face_encodings(img, _face_location)  # or here !
    print(_face_location, face_encoding)