from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from connector.connDB import connDB
from material.Label import LblNull
from material.PushButton import BtnTool
from material.PushButton import BtnTabClose
from component.dialog.DialogMassage import DialogMassage
from component.table.TableTimeUser import TableTimeUser
from component.table.TableTimeBusiness import TableTimeBusiness
from component.table.TableTimeHeader import TableTimeHeader
from component.table.TableTimeTotal import TableTimeTotal
from method.valueTran import returnTranValue
from qss.Dialog import styleGeneral
from datetime import datetime


class MainUserTime(QWidget):
    def __init__(self, windows):
        QWidget.__init__(self)
        self.setStyleSheet(styleGeneral)
        self.windows = windows
        self.account = windows.account
        self.year = windows.CURRENT_YEAR
        self.__connector__()
        self.__component__()
        self.btnToday.click()

    def __connector__(self):
        self.connDB = connDB(self.year)

    def __component__(self):
        self.__pushButton__()
        self.__table__()
        self.__scrollBar__()
        self.__layout__()

    def __pushButton__(self):
        def btnCloseClick():
            idx = self.windows.tab.currentIndex()
            self.windows.tab.removeTab(idx)
            self.windows.currentTabs.pop(idx)
        self.btnClose = BtnTabClose('닫기\n(Ctrl+W)', btnCloseClick)

        def btnSaveClick():
            cnt = 0
            for obj in self.tblTime.objects:
                if obj.editLog:
                    column = self.tblTime.horizontalHeaderItem(obj.col).text()
                    value = obj.data
                    number = self.tblTime.item(obj.row, 0).text()
                    option = self.tblTime.item(obj.row, 3).text()
                    self.connDB.updateUserTime(column, value, number, option, self.account)
                    obj.init = value
                    obj.editLog = False
                    cnt += 1
            if cnt:
                DialogMassage('저장되었습니다.')
        self.btnSave = BtnTool('저장\n(Ctrl+S)', btnSaveClick, shortcut='Ctrl+S')

        def btnTodayClick():
            today = datetime.today()
            today = today.strftime("%m/%d")
            for col, header in enumerate(self.tblTime.columns):
                if today in header:
                    self.tblTime.setCurrentCell(0, col)
                    break
        self.btnToday = BtnTool('오늘\n(Ctrl+T)', btnTodayClick, shortcut='Ctrl+T')

        def btnRefreshClick():
            self.windows.RefreshTimeUser()
        self.btnRefresh = BtnTool('새로고침\n(F5)', btnRefreshClick, shortcut='F5')

        def btnExcelClick():
            dig = QFileDialog()
            filePath = dig.getSaveFileName(caption='엑셀로 내보내기', filter='*.xlsx')[0]
            if filePath != '':
                df = self.connDB.dataFramePerUserTime(self.account)
                del df['적용상태_사업']
                del df['계정']
                del df['성명']
                del df['적용상태_부서원']
                df.to_excel(filePath, sheet_name=f'{self.year}-{self.account}', index=False)
                DialogMassage(f'저장되었습니다.\n\n○ 파일 경로 : {filePath}')
        self.btnExcel = BtnTool('엑셀로 저장\n(Ctrl+E)', btnExcelClick)

    def __table__(self):
        self.tblBusiness = TableTimeBusiness(self.account, self.year)
        self.tblTime = TableTimeUser(self.account, self.year, self)
        self.tblHeader = TableTimeHeader()
        self.tblHeader.setColumnWidth(0, self.tblBusiness.width)
        self.tblHeader.setFixedWidth(self.tblBusiness.width)
        self.tblHeader.setFixedHeight(self.tblHeader.rowHeight(0))
        self.tblTotal = TableTimeTotal(self.account, self.year, self.tblTime.columns[8:])
        self.tblTotal.setFixedHeight(self.tblHeader.rowHeight(0))

    def __scrollBar__(self):
        def verScrBusinessChange(value):
            self.verScrTime.setValue(value)
        self.verScrBusiness = self.tblBusiness.verticalScrollBar()
        self.verScrBusiness.valueChanged.connect(verScrBusinessChange)

        def verScrTimeChange(value):
            self.verScrBusiness.setValue(value)
        self.verScrTime = self.tblTime.verticalScrollBar()
        self.verScrTime.valueChanged.connect(verScrTimeChange)

        def horScrTimeChange(value):
            self.horScrTotal.setValue(value)
        self.horScrTime = self.tblTime.horizontalScrollBar()
        self.horScrTime.valueChanged.connect(horScrTimeChange)

        def horScrTotalChange(value):
            self.horScrTime.setValue(value)
        self.horScrTotal = self.tblTotal.horizontalScrollBar()
        self.horScrTotal.valueChanged.connect(horScrTotalChange)

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnSave)
        layoutBtn.addWidget(self.btnToday)
        layoutBtn.addWidget(self.btnRefresh)
        layoutBtn.addWidget(self.btnExcel)
        layoutBtn.addWidget(LblNull(), 10)
        layoutTop = QHBoxLayout()
        layoutTop.addWidget(self.tblHeader)
        layoutTop.addWidget(self.tblTotal)
        layoutBottom = QHBoxLayout()
        layoutBottom.addWidget(self.tblBusiness)
        layoutBottom.addWidget(self.tblTime)
        layoutTbl = QVBoxLayout()
        layoutTbl.addLayout(layoutTop)
        layoutTbl.addLayout(layoutBottom)
        layoutTbl.addWidget(self.horScrTime)
        layoutScr = QHBoxLayout()
        layoutScr.addLayout(layoutTbl)
        layoutScr.addWidget(self.verScrTime)
        layout = QVBoxLayout()
        layout.addLayout(layoutBtn)
        layout.addLayout(layoutScr)
        self.setLayout(layout)

    def changeTotalValue(self, _):
        ldtTime = self.sender()
        table = ldtTime.table
        values = []
        for row in range(self.tblTime.rowCount()):
            value = table.cellWidget(row, ldtTime.col).text()
            try:
                value = float(value)
            except:
                value = 0.0
            values.append(value)
        total = returnTranValue(sum(values))
        self.tblTotal.cellWidget(0, ldtTime.col-8).setText(str(total))

    def keyPressEvent(self, QKeyEvent):
        if Qt.ControlModifier:
            if QKeyEvent.key() == Qt.Key_S:
                self.btnSave.click()
            elif QKeyEvent.key() == Qt.Key_T:
                self.btnToday.click()
            elif QKeyEvent.key() == Qt.Key_E:
                self.btnExcel.click()
            elif QKeyEvent.key() == Qt.Key_W:
                self.btnClose.click()
        elif QKeyEvent.key() == Qt.Key_F5:
            self.btnRefresh.click()
