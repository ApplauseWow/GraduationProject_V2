import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QWidget, QGridLayout
from PyQt5 import QtCore
from main_win import Ui_MainWindow
from id_info_win import Ui_id_info_win
from ui_finish import MainWindow, InfoWindow, WarningWindow, RegisterWindow, ManagementWindow, Pagination


class ui(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(ui, self).__init__()
        self.setupUi(self)

class ui2(QDialog, Ui_id_info_win):
    def __init__(self):
        super(ui2, self).__init__()
        self.setupUi(self)
        map(lambda x: x.setStyleSheet("QLabel{"
                                      "                   background-color:rgba(84,140,255,150);"
                                      "                   border-style:outset;                  "
                                      "                   border-width:4px;                     "
                                      "                   border-radius:10px;                "
                                      "                   border-color:rgba(255,255,255,30);   "
                                      "                   font:bold 18px;                    "
                                      "                   color:rgba(0,0,0,100);                "
                                      "                   padding:6px;                       "
                                      "                   }"),
            [self.l_id, self.l_name, self.l_type, self.user_id, self.user_name, self.user_type])
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win_ = MainWindow()
    win_.show()
    win = InfoWindow()
    win.show()
    win1 = WarningWindow()
    win1.show()
    win2 = RegisterWindow()
    win2.show()
    # exec("bt_{} = QPushButton()".format("close"))
    # print bt_close
    # win3 = ManagementWindow(201610414206, 1)
    # w = QWidget()
    # y = QGridLayout()
    # page = Pagination()
    # p2 = Pagination()
    # y.addWidget(page, 0, 0, 5, 9)
    # y.addWidget(p2, 0, 5, 5, 9)
    # w.setLayout(y)
    # win3.right_layout.addWidget(w)
    # win4 = Pagination()
    # win4.show()
    sys.exit(app.exec_())

"style sheet"
'''
"QPushButton{"
"                   background-color:rgba(84,140,255,30);"
"                   border-style:outset;                  "
"                   border-width:4px;                     "
"                   border-radius:10px;                "
"                   border-color:rgba(255,255,255,30);   "
"                   font:bold 18px;                    "
"                   color:rgba(0,0,0,100);                "
"                   padding:6px;                       "
"                   }"
"                   QPushButton:pressed{"
"                   background-color:rgba(84,140,255,200);"
"                   border-color:rgba(255,255,255,30);"
"                   border-style:inset;"
"                   color:rgba(0,0,0,100);"
"                   }"
"                   QPushButton:hover{"
"                   background-color:rgba(84,140,255,100);"
"                   border-color:rgba(255,255,255,200);"
"                   color:rgba(0,0,0,200);"
"                   }"
'''