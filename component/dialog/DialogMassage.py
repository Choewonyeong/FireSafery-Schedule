from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from material.Label import LblMessage
from material.PushButton import BtnOk
from material.PushButton import BtnNo
from material.PushButton import BtnYes
from qss.Dialog import styleGeneral


class DialogMassage(QDialog):
    def __init__(self, text, question=False):
        QDialog.__init__(self)
        self.setStyleSheet(styleGeneral)
        self.text = text
        self.question = question
        self.value = False
        self.__setting__()
        self.__component__()
        self.exec_()

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

        def btnYesClick():
            self.value = True
            self.close()
        self.btnYes = BtnYes('예', btnYesClick)
        self.btnYes.setFixedWidth(80)

        def btnNoClick():
            self.value = False
            self.close()
        self.btnNo = BtnNo('아니오', btnNoClick)
        self.btnNo.setFixedWidth(80)

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        if self.question:
            self.btnNo.setDefault(True)
            layoutBtn.addWidget(self.btnNo)
            layoutBtn.addWidget(self.btnYes)
        elif not self.question:
            self.btnOk.setDefault(True)
            layoutBtn.addWidget(self.btnOk)
        layout = QVBoxLayout()
        layout.addWidget(self.lblText)
        layout.addLayout(layoutBtn)
        self.setLayout(layout)
