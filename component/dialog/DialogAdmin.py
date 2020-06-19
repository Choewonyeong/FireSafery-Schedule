from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from material.Label import LblMessage
from material.LineEdit import LdtEditPasswordLeft
from material.PushButton import BtnNo
from material.PushButton import BtnYes
from component.dialog.DialogPassword import DialogPassword
from component.dialog.DialogMassage import DialogMassage
from qss.Dialog import styleGeneral


class DialogAdmin(QDialog):
    def __init__(self, account, row, table):
        QDialog.__init__(self)
        self.setStyleSheet(styleGeneral)
        self.account = account
        self.row = row
        self.table = table
        self.__setting__()
        self.__variables__()
        self.__component__()
        self.exec_()

    def __setting__(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(350)

    def __variables__(self):
        self.password = ''
        self.adminPasswords = self.table.widget.windows.connUser.returnAdminPassword()

    def __component__(self):
        self.__label__()
        self.__lineEdit__()
        self.__pushButton__()
        self.__layout__()

    def __label__(self):
        self.lblPassword = LblMessage('관리자의 권한이 필요합니다.\n비밀번호를 입력하세요.')

    def __lineEdit__(self):
        self.ldtPassword = LdtEditPasswordLeft()

    def __pushButton__(self):
        def btnCloseClick():
            self.close()
        self.btnClose = BtnNo('닫기', btnCloseClick)

        def btnConfirmClick():
            password = self.ldtPassword.text()
            if password in self.adminPasswords:
                userName = self.connUser.returnName(self.account)
                userPassword = self.connUser.returnPassword(self.account)
                self.close()
                DialogPassword(userName, self.account, userPassword, self.row, self.table)
            else:
                DialogMassage('비밀번호가 맞지 않습니다.')
        self.btnConfirm = BtnYes('확인', btnConfirmClick, default=True, shortcut='return')

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnConfirm)
        layout = QVBoxLayout()
        layout.addWidget(self.lblPassword)
        layout.addWidget(self.ldtPassword)
        layout.addLayout(layoutBtn)
        self.setLayout(layout)
