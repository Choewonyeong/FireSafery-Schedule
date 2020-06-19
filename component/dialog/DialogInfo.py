from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from material.Label import LblMessage
from material.PushButton import BtnOk
from qss.Dialog import styleGeneral


class DialogInfo(QDialog):

    def __init__(self, text):
        QDialog.__init__(self)
        self.setStyleSheet(styleGeneral)
        self.text = text
        self.__setting__()
        self.__component__()
        self.show()

    def __setting__(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setFixedWidth(350)

    def __component__(self):
        self.__label__()
        self.__pushButton__()
        self.__layout__()

    def __label__(self):
        self.lblText = LblMessage(self.text)

    def __pushButton__(self):
        def btnOkClick():
            self.value = False
            self.close()
        self.btnOk = BtnOk('확인', btnOkClick)
        self.btnOk.setFixedWidth(80)

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        self.btnOk.setDefault(True)
        layoutBtn.addWidget(self.btnOk)
        layout = QVBoxLayout()
        layout.addWidget(self.lblText)
        layout.addLayout(layoutBtn)
        self.setLayout(layout)
