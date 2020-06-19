from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from component.dialog.DialogNewInfo import DialogNewInfo
from component.table.TableAdminInfo import TableAdminInfo
from material.PushButton import BtnTabClose
from material.PushButton import BtnTool
from material.Label import LblNull


class MainAdminInfo(QDialog):
    def __init__(self, windows):
        QDialog.__init__(self)
        self.windows = windows
        self.__component__()

    def __component__(self):
        self.__button__()
        self.__table__()
        self.__layout__()

    def __button__(self):
        def btnCloseClick():
            idx = self.windows.tab.currentIndex()
            self.windows.tab.removeTab(idx)
            self.windows.currentTabs.pop(idx)
        self.btnClose = BtnTabClose('닫기\n(Ctrl+W)', btnCloseClick)

        def btnRefreshClick():
            self.windows.RefreshAdminInfo()
        self.btnRefresh = BtnTool('새로고침\n(F5)', btnRefreshClick, shortcut='F5')

        def btnNewClick():
            DialogNewInfo(self.windows)
        self.btnNew = BtnTool('새 알림\n(Ctrl+N)', btnNewClick, shortcut='Ctrl+N')

    def __table__(self):
        self.tbl = TableAdminInfo(self)

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnNew)
        layoutBtn.addWidget(LblNull(), 10)
        layout = QVBoxLayout()
        layout.addLayout(layoutBtn)
        layout.addWidget(self.tbl)
        self.setLayout(layout)

    def keyPressEvent(self, QKeyEvent):
        if Qt.ControlModifier:
            if QKeyEvent.key() == Qt.Key_W:
                self.btnClose.click()
            elif QKeyEvent.key() == Qt.Key_N:
                self.btnClose.click()
        elif QKeyEvent.key() == Qt.Key_F5:
            self.btnRefresh.click()

