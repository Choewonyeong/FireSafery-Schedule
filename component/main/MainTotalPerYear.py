from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from material.PushButton import BtnTabClose
from material.PushButton import BtnTool
from material.Label import LblNull
from component.table.TableTotalPerYear import TableTotalPerYear
from component.dialog.DialogMassage import DialogMassage


class MainTotalPerYear(QWidget):
    def __init__(self, windows):
        QWidget.__init__(self)
        self.windows = windows
        self.__component__()

    def __component__(self):
        self.__pushButton__()
        self.__table__()
        self.__layout__()

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
                df = self.tbl.dataFrame
                df.to_excel(filePath, sheet_name=f'연도별시간집계', index=False)
                DialogMassage(f'저장되었습니다.\n\n○ 파일 경로 : {filePath}')
        self.btnExcel = BtnTool('엑셀로 저장\n(Ctrl+E)', btnExcelClick)

        def btnRefreshClick():
            self.windows.RefreshTotalPerYear()
        self.btnRefresh = BtnTool('새로고침\n(F5)', btnRefreshClick)

    def __table__(self):
        self.tbl = TableTotalPerYear()

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnExcel)
        layoutBtn.addWidget(self.btnRefresh)
        layoutBtn.addWidget(LblNull(), 10)
        layout = QVBoxLayout()
        layout.addLayout(layoutBtn)
        layout.addWidget(self.tbl)
        self.setLayout(layout)

    def keyPressEvent(self, QKeyEvent):
        if Qt.ControlModifier:
            if QKeyEvent.key() == Qt.Key_E:
                self.btnExcel.click()
            elif QKeyEvent.key() == Qt.Key_W:
                self.btnClose.click()
        elif QKeyEvent.key() == Qt.Key_F5:
            self.btnRefresh.click()
