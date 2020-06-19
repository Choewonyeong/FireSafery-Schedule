from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from component.dialog.DialogMassage import DialogMassage
from component.table.TableDBUser import TableDBUser
from component.table.TableDBBusiness import TableDBBusiness
from material.Label import LblNull
from material.Label import LblTitle
from material.ComboBox import CbxYears
from material.PushButton import BtnTool
from material.PushButton import BtnCreateNewDB
from material.PushButton import BtnTabClose
from method.dbList import returnMainList
from pandas import ExcelWriter


class MainDatabase(QWidget):
    def __init__(self, windows):
        QWidget.__init__(self)
        self.windows = windows
        self.__component__()

    def __component__(self):
        self.__comboBox__()
        self.__pushButton__()
        self.__table__()
        self.__label__()
        self.__layout__()

    def __comboBox__(self):
        def cbxYearChange(text):
            self.windows.DB_YEAR = text
            self.windows.RefreshAdminDB()
        self.cbxYear = CbxYears(returnMainList(), self.windows.DB_YEAR)
        self.cbxYear.currentTextChanged.connect(cbxYearChange)

    def __pushButton__(self):
        def btnCloseClick():
            idx = self.windows.tab.currentIndex()
            self.windows.tab.removeTab(idx)
            self.windows.currentTabs.pop(idx)
        self.btnClose = BtnTabClose('닫기\n(Ctrl+W)', btnCloseClick)

        nextYear = f'{int(self.cbxYear.currentText())+1}'
        self.btnCreate = BtnCreateNewDB(f'{nextYear}년 생성\n(Ctrl+N)', shortcut='Ctrl+N', windows=self.windows)

        def btnExcelClick():
            currentYear = self.cbxYear.currentText()
            dig = QFileDialog(self)
            filePath = dig.getSaveFileName(caption="엑셀로 내보내기", directory='', filter='*.xlsx')[0]
            if filePath != '':
                with ExcelWriter(filePath) as writer:
                    dataFrame = self.tblUser.dataFrame
                    dataFrame.to_excel(writer, sheet_name=f"화재팀-DB 현황({currentYear}-부서원)", index=False)
                    dataFrame = self.tblBusiness.dataFrame
                    dataFrame.to_excel(writer, sheet_name=f"화재팀-DB 현황({currentYear}-사업)", index=False)
                writer.close()
                DialogMassage('엑셀로 내보내기가 완료되었습니다.')
        self.btnExcel = BtnTool('엑셀로 저장\n(Ctrl+E)', btnExcelClick, shortcut='Ctrl+E')

        def btnRefreshClick():
            self.windows.RefreshAdminDB()
        self.btnRefresh = BtnTool('새로고침\n(F5)', btnRefreshClick)

    def __table__(self):
        self.tblUser = TableDBUser(self.windows.DB_YEAR, self)
        self.tblBusiness = TableDBBusiness(self.windows.DB_YEAR, self)

    def __label__(self):
        self.cntTotalUser = len(self.tblUser.dataFrame['적용상태_부서원'].tolist())
        self.cntAcceptUser = self.tblUser.dataFrame['적용상태_부서원'].tolist().count('적용')
        self.lblUser = LblTitle(f'○ 적용상태 / 총 부서원 수 : {self.cntAcceptUser}명 / {self.cntTotalUser}명')
        self.cntTotalBusiness = len(self.tblBusiness.dataFrame['적용상태_사업'].tolist())
        self.cntAcceptBusiness = self.tblBusiness.dataFrame['적용상태_사업'].tolist().count('적용')
        self.lblBusiness = LblTitle(f'○ 적용상태 / 총 사업 수 : {self.cntAcceptBusiness}건 / {self.cntTotalBusiness}건')

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.cbxYear)
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnCreate)
        layoutBtn.addWidget(self.btnExcel)
        layoutBtn.addWidget(self.btnRefresh)
        layoutBtn.addWidget(LblNull(), 10)
        layoutTblUser = QVBoxLayout()
        layoutTblUser.addWidget(self.lblUser)
        layoutTblUser.addWidget(self.tblUser)
        layoutTblBusiness = QVBoxLayout()
        layoutTblBusiness.addWidget(self.lblBusiness)
        layoutTblBusiness.addWidget(self.tblBusiness)
        layoutTbl = QHBoxLayout()
        layoutTbl.addLayout(layoutTblUser)
        layoutTbl.addLayout(layoutTblBusiness)
        layoutTbl.addWidget(LblNull(), 10)
        layout = QVBoxLayout()
        layout.addLayout(layoutBtn)
        layout.addLayout(layoutTbl)
        self.setLayout(layout)

    def keyPressEvent(self, QKeyEvent):
        if Qt.ControlModifier:
            if QKeyEvent.key() == Qt.Key_N:
                self.btnCreate.click()
            elif QKeyEvent.key() == Qt.Key_E:
                self.btnExcel.click()
            elif QKeyEvent.key() == Qt.Key_W:
                self.btnClose.click()
        elif Qt.Key_F5:
            self.btnRefresh.click()
