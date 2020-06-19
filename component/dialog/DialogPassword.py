from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from material.Label import LblSignup
from material.Label import LblInformation
from material.LineEdit import LdtEditPasswordRight
from material.PushButton import BtnNo
from material.PushButton import BtnYes
from component.dialog.DialogMassage import DialogMassage
from qss.Dialog import styleGeneral


class DialogPassword(QDialog):
    def __init__(self, name, account, password, row, table):
        QDialog.__init__(self)
        self.setStyleSheet(styleGeneral)
        self.row = row
        self.table = table
        self.name = name
        self.account = account
        self.password = password
        self.__setting__()
        self.__component__()
        self.exec_()

    def __setting__(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(350)

    def __component__(self):
        self.__label__()
        self.__lineEdit__()
        self.__pushButton__()
        self.__layout__()

    def __label__(self):
        self.lblAccount = LblInformation(f"ID : {self.account}")
        self.lblName = LblInformation(f"성명 : {self.name}")
        self.lblPassword = LblInformation(f"비밀번호 : {self.password}")
        self.lblChange = LblSignup('새 비밀번호')
        self.lblChangeConfirm = LblSignup('새 비밀번호 확인')

    def __lineEdit__(self):
        self.ldtChange = LdtEditPasswordRight()
        self.ldtChangeConfirm = LdtEditPasswordRight()

    def __pushButton__(self):
        def btnCloseClick():
            self.close()
        self.btnClose = BtnNo('닫기', btnCloseClick)
        self.btnClose.clicked.connect(btnCloseClick)

        def btnApplyClick():
            newPassword = self.ldtChange.text()
            newPasswordConfirm = self.ldtChangeConfirm.text()
            if newPassword == '':
                DialogMassage('비밀번호를 입력하세요.')
            elif newPassword != newPasswordConfirm:
                DialogMassage('비밀번호가 일치하지 않습니다.')
            elif newPassword == self.password:
                DialogMassage('기존의 비밀번호와 동일합니다.')
            else:
                self.table.UpdateEditDate(self.row, self.table.widget.windows.connUser.updatePassword(self.account, newPassword))
                DialogMassage(f'{self.name}님의 비밀번호가 변경되었습니다.')
                self.close()
        self.btnApply = BtnYes('변경', btnApplyClick, default=True, shortcut='return')

    def __layout__(self):
        layoutChange = QHBoxLayout()
        layoutChange.addWidget(self.lblChange)
        layoutChange.addWidget(self.ldtChange)
        layoutChangeConfirm = QHBoxLayout()
        layoutChangeConfirm.addWidget(self.lblChangeConfirm)
        layoutChangeConfirm.addWidget(self.ldtChangeConfirm)
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnApply)
        layout = QVBoxLayout()
        layout.addWidget(self.lblAccount)
        layout.addWidget(self.lblName)
        layout.addWidget(self.lblPassword)
        layout.addLayout(layoutChange)
        layout.addLayout(layoutChangeConfirm)
        layout.addLayout(layoutBtn)
        self.setLayout(layout)
