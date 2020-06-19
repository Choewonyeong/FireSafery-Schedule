from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from material.ComboBox import CbxYears
from material.PushButton import BtnTabClose
from material.PushButton import BtnTool
from material.Label import LblNull
from component.table.TableTotalPerUser import TableTotalPerUser
from component.dialog.DialogMassage import DialogMassage
from method.totalList import returnTotalPerUser
from pandas import ExcelWriter
from os import listdir
import setting


class MainTotalPerUser(QWidget):
    def __init__(self, windows):
        QWidget.__init__(self)
        self.windows = windows
        self.__component__()

    def __component__(self):
        self.__comboBox__()
        self.__pushButton__()
        self.__variables__()
        self.__table__()
        self.__tab__()
        self.__layout__()

    def __comboBox__(self):
        years = listdir(setting.databaseMain)
        years = [year.replace('.db', '') for year in years]

        def cbxYearChange(text):
            self.windows.TOTAL_YEAR = text
            self.windows.RefreshTotalPerUser()
        self.cbxYear = CbxYears(years, self.windows.TOTAL_YEAR)
        self.cbxYear.currentTextChanged.connect(cbxYearChange)

    def __pushButton__(self):
        def btnCloseClick():
            idx = self.windows.tab.currentIndex()
            self.windows.tab.removeTab(idx)
            self.windows.currentTabs.pop(idx)
        self.btnClose = BtnTabClose('닫기\n(Ctrl+W)', btnCloseClick)

        def btnExcelClick():
            dig = QFileDialog()
            filePath = dig.getSaveFileName(caption='엑셀로 내보내기', filter='*.xlsx')[0]
            if filePath != '':
                with ExcelWriter(filePath) as writer:
                    for key in self.totalDict.keys():
                        df = self.totalDict[key]
                        df.to_excel(writer, sheet_name=key, index=False)
                writer.close()
                DialogMassage(f'저장되었습니다.\n\n○ 파일 경로 : {filePath}')
        self.btnExcel = BtnTool('엑셀로 저장\n(Ctrl+E)', btnExcelClick)

        def btnRefreshClick():
            self.windows.RefreshTotalPerUser()
        self.btnRefresh = BtnTool('새로고침\n(F5)', btnRefreshClick)

    def __variables__(self):
        self.columns = returnTotalPerUser(self.windows.TOTAL_YEAR, column=True)
        self.totalDict = returnTotalPerUser(self.windows.TOTAL_YEAR)

    def __table__(self):
        self.objectTable = []
        for userName in self.totalDict.keys():
            self.objectTable.append(TableTotalPerUser(self, userName))

    def __tab__(self):
        self.tab = QTabWidget()
        self.tab.addTab(self.objectTable[-1], self.objectTable[-1].userName)
        self.objectTable.pop()
        currentText = []
        for table in self.objectTable:
            currentText.append(table.userName)
            self.tab.addTab(table, table.userName)
        self.tab.setCurrentIndex(currentText.index(self.windows.connUser.returnName(self.windows.account))+1)

    def __layout__(self):
        layoutTop = QHBoxLayout()
        layoutTop.addWidget(self.cbxYear)
        layoutTop.addWidget(self.btnClose)
        layoutTop.addWidget(self.btnExcel)
        layoutTop.addWidget(self.btnRefresh)
        layoutTop.addWidget(LblNull(), 10)
        layout = QVBoxLayout()
        layout.addLayout(layoutTop)
        layout.addWidget(self.tab)
        self.setLayout(layout)

    def keyPressEvent(self, QKeyEvent):
        if Qt.ControlModifier:
            if QKeyEvent.key() == Qt.Key_E:
                self.btnExcel.click()
            elif QKeyEvent.key() == Qt.Key_W:
                self.btnClose.click()
        elif QKeyEvent.key() == Qt.Key_F5:
            self.btnRefresh.click()
