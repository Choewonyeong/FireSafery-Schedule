from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from component.table.TableAdminUser import TableAdminUser
from component.dialog.DialogMassage import DialogMassage
from material.Label import LblNull
from material.Label import LblTitle
from material.PushButton import BtnTool
from material.PushButton import BtnTabClose


class MainAdminUser(QWidget):
    def __init__(self, windows):
        QWidget.__init__(self)
        self.windows = windows
        self.__component__()

    def __component__(self):
        self.__pushButton__()
        self.__table__()
        self.__label__()
        self.__layout__()

    def __pushButton__(self):
        def btnCloseClick():
            idx = self.windows.tab.currentIndex()
            self.windows.tab.removeTab(idx)
            self.windows.currentTabs.pop(idx)
        self.btnClose = BtnTabClose('닫기\n(Ctrl+W)', btnCloseClick)

        def btnSaveClick():
            saveValue = 0
            for obj in self.tbl.objects:
                if obj.editLog:
                    self.tbl.UpdateEditDate(obj.row, self.windows.connUser.updateUser(obj.header, obj.data, obj.number))
                    obj.init = obj.data
                    obj.editLog = False
                    saveValue += 1
            if saveValue:
                DialogMassage('저장되었습니다.')
                self.windows.RefreshAdminUser()
        self.btnSave = BtnTool('저장\n(Ctrl+S)', btnSaveClick, shortcut='Ctrl+S')

        def btnRefreshClick():
            self.windows.RefreshAdminUser()
        self.btnRefresh = BtnTool('새로고침\n(F5)', btnRefreshClick, shortcut='F5')

        def btnExcelClick():
            dig = QFileDialog()
            filePath = dig.getSaveFileName(caption='엑셀로 내보내기', filter='*.xlsx')[0]
            if filePath != '':
                df = self.windows.connUser.dataFrameUser()
                del df[self.tbl.columns[14]]
                del df[self.tbl.columns[2]]
                df.to_excel(filePath, sheet_name=f'화재안전팀 부서원 현황(상세)', index=False)
                DialogMassage(f'저장되었습니다.\n\n○ 파일 경로 : {filePath}')
        self.btnExcel = BtnTool('엑셀로 저장\n(Ctrl+E)', btnExcelClick)

    def __table__(self):
        self.tbl = TableAdminUser(self)

    def __label__(self):
        cnt = len(self.tbl.dataFrame)
        cnt = 0 if cnt < 0 else cnt
        self.lblCount = LblTitle(f"총 부서원 수 : {cnt}명")

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnSave)
        layoutBtn.addWidget(self.btnRefresh)
        layoutBtn.addWidget(self.btnExcel)
        layoutBtn.addWidget(LblNull(), 10)
        layout = QVBoxLayout()
        layout.addLayout(layoutBtn)
        layout.addWidget(self.lblCount)
        layout.addWidget(self.tbl)
        self.setLayout(layout)

    def keyPressEvent(self, QKeyEvent):
        if Qt.ControlModifier:
            if QKeyEvent.key() == Qt.Key_S:
                self.btnSave.click()
            if QKeyEvent.key() == Qt.Key_E:
                self.btnExcel.click()
            elif QKeyEvent.key() == Qt.Key_W:
                self.btnClose.click()
        elif QKeyEvent.key() == Qt.Key_F5:
            self.btnRefresh.click()