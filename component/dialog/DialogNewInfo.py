from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from component.dialog.DialogMassage import DialogMassage
from qss.Dialog import styleGeneral
from material.ComboBox import CbxNewInfo
from material.GroupBox import GbxSelectDateTime
from material.Label import LblNewInfo
from material.LineEdit import LdtNewInfo
from material.PushButton import BtnCancel
from material.PushButton import BtnSubmit
from material.TextEdit import TdtInfo
from setting.variables import itemInfoOption
from setting.variables import itemInfoUsed
from setting.variables import itemInfoTarget


class DialogNewInfo(QDialog):
    def __init__(self, windows):
        QDialog.__init__(self)
        self.setStyleSheet(styleGeneral)
        self.windows = windows
        self.__setting__()
        self.__component__()
        self.exec_()

    def __setting__(self):
        self.setWindowFlag(Qt.FramelessWindowHint)

    def __component__(self):
        self.__label__()
        self.__inputWidgets__()
        self.__pushButton__()
        self.__layout__()

    def __label__(self):
        lblNumber = LblNewInfo('번호')
        lblTitle = LblNewInfo('구분')
        lblText = LblNewInfo('내용')
        lblUsed = LblNewInfo('사용여부')
        lblTarget = LblNewInfo('대상')
        lblStart = LblNewInfo('시작일')
        lblEnd = LblNewInfo('종료일')
        self.objectLabel = [lblNumber,
                            lblTitle,
                            lblText,
                            lblUsed,
                            lblTarget,
                            lblStart,
                            lblEnd]

    def __inputWidgets__(self):
        number = self.windows.connInfo.returnNumber()
        inputNumber = LdtNewInfo(text=number, enabled=False)
        inputOption = CbxNewInfo(items=itemInfoOption)
        inputText = TdtInfo()
        inputUsed = CbxNewInfo(items=itemInfoUsed)
        inputTarget = CbxNewInfo(items=itemInfoTarget)
        groupBoxStart = GbxSelectDateTime(self.windows)
        groupBoxEnd = GbxSelectDateTime(self.windows)
        self.objectInput = [inputNumber,
                            inputOption,
                            inputText,
                            inputUsed,
                            inputTarget,
                            groupBoxStart,
                            groupBoxEnd]

    def __pushButton__(self):
        def btnCloseClick():
            self.close()
        self.btnClose = BtnCancel('닫기', btnCloseClick)

        def btnInsertClick():
            from datetime import datetime
            infoInfo = []
            for idx, info in enumerate(self.objectInput):
                if idx == 0:
                    infoInfo.append(info.text())
                elif idx in [1, 3, 4]:
                    infoInfo.append(info.currentText())
                elif idx == 2:
                    infoInfo.append(info.toPlainText())
                elif idx in [5, 6]:
                    infoInfo.append(info.date)
            if infoInfo[2] == '':
                DialogMassage('내용을 입력하세요.')
            elif datetime.strptime(infoInfo[5], "%Y-%m-%d") > datetime.strptime(infoInfo[6], "%Y-%m-%d"):
                DialogMassage('시작일 또는 종료일을 확인하세요.')
            else:
                self.windows.connInfo.insertInfo(infoInfo)
                self.windows.RefreshAdminInfo()
                self.close()
                DialogMassage('새로운 알림 정보가 등록되었습니다.')
        self.btnInsert = BtnSubmit('등록', btnInsertClick, default=True)

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnInsert)
        layout = QVBoxLayout()
        for lbl, widget in zip(self.objectLabel, self.objectInput):
            layoutObjects = QHBoxLayout()
            layoutObjects.addWidget(lbl)
            layoutObjects.addWidget(widget)
            layout.addLayout(layoutObjects)
        layout.addLayout(layoutBtn)
        self.setLayout(layout)
