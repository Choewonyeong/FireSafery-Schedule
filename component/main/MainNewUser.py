from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from material.Label import LblNull
from material.PushButton import BtnTool
from material.PushButton import BtnTabClose
from component.table.TableNewUser import TableNewUser


class MainNewUser(QWidget):
    def __init__(self, windows):
        QWidget.__init__(self)
        self.windows = windows
        self.__variables__()
        self.__component__()

    def __variables__(self):
        self.columns = self.windows.connUser.dataFrameSignup(column=True)+['', '']
        self.columns[self.columns.index('수정한날짜')] = '가입신청일자'
        self.dataFrame = self.windows.connUser.dataFrameSignup()

    def __component__(self):
        self.__pushButton__()
        self.__table__()
        self.__tableLayout__()

    def __pushButton__(self):
        def btnCloseClick():
            idx = self.windows.tab.currentIndex()
            self.windows.tab.removeTab(idx)
            self.windows.currentTabs.pop(idx)
        self.btnClose = BtnTabClose('닫기(Esc)', btnCloseClick)

        def btnRefreshClick():
            self.windows.RefreshNewUser()
        self.btnRefresh = BtnTool('새로고침(F5)', btnRefreshClick)

    def __table__(self):
        self.tblNewUser = TableNewUser(self)

    def __tableLayout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnRefresh)
        layoutBtn.addWidget(LblNull(), 10)
        layout = QVBoxLayout()
        layout.addLayout(layoutBtn)
        layout.addWidget(self.tblNewUser)
        self.setLayout(layout)

