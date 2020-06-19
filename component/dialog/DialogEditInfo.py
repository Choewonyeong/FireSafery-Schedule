from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
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


class DialogEditInfo(QDialog):
    def __init__(self, windows, table, row):
        QDialog.__init__(self)
        self.setStyleSheet(styleGeneral)
        self.windows = windows
        self.table = table
        self.row = row
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
        number = self.table.item(self.row, 0).text()
        option = self.table.item(self.row, 1).text()
        text = self.table.item(self.row, 2).text()
        use = self.table.item(self.row, 3).text()
        target = self.table.item(self.row, 4).text()
        startYear = self.table.item(self.row, 5).text()[:4]
        startMonth = self.table.item(self.row, 5).text()[5:7]
        startDay = self.table.item(self.row, 5).text()[8:]
        endYear = self.table.item(self.row, 6).text()[:4]
        endMonth = self.table.item(self.row, 6).text()[5:7]
        endDay = self.table.item(self.row, 6).text()[8:]
        self.values = [number,
                       option,
                       text,
                       use,
                       target,
                       f"{startYear}-{startMonth}-{startDay}",
                       f"{endYear}-{endMonth}-{endDay}"]
        inputNumber = LdtNewInfo(text=number, enabled=False)
        inputOption = CbxNewInfo(items=itemInfoOption, text=option)
        inputText = TdtInfo(text=text)
        inputUsed = CbxNewInfo(items=itemInfoUsed, text=use)
        inputTarget = CbxNewInfo(items=itemInfoTarget, text=target)
        groupBoxStart = GbxSelectDateTime(self.windows, startYear, startMonth, startDay)
        groupBoxEnd = GbxSelectDateTime(self.windows, endYear, endMonth, endDay)
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

        def btnSaveClick():
            from datetime import datetime
            infoInfo = [self.objectInput[0].text(),
                        self.objectInput[1].currentText(),
                        self.objectInput[2].toPlainText(),
                        self.objectInput[3].currentText(),
                        self.objectInput[4].currentText(),
                        self.objectInput[5].date,
                        self.objectInput[6].date]
            indexes = []
            for idx in range(len(infoInfo)):
                if self.values[idx] != infoInfo[idx]:
                    indexes.append(idx)
            if indexes:
                if infoInfo[2] == '':
                    DialogMassage('내용을 입력하세요.')
                elif datetime.strptime(infoInfo[5], "%Y-%m-%d") > datetime.strptime(infoInfo[6], "%Y-%m-%d"):
                    DialogMassage('시작일 또는 종료일을 확인하세요.')
                else:
                    number = infoInfo[0]
                    for idx in indexes:
                        header = self.objectLabel[idx].text()
                        data = infoInfo[idx]
                        self.windows.connInfo.updateInfo(header, data, number)
                    self.windows.RefreshAdminInfo()
                    DialogMassage('알림 정보가 수정되었습니다.')
        self.btnSave = BtnSubmit('저장', btnSaveClick, default=True)

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnSave)
        layout = QVBoxLayout()
        for lbl, widget in zip(self.objectLabel, self.objectInput):
            layoutObjects = QHBoxLayout()
            layoutObjects.addWidget(lbl)
            layoutObjects.addWidget(widget)
            layout.addLayout(layoutObjects)
        layout.addLayout(layoutBtn)
        self.setLayout(layout)
