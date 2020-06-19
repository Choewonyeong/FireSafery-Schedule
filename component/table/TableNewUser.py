from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from connector.connDB import connDB
from material.PushButton import BtnAcceptInTable
from material.PushButton import BtnRejectInTable
from component.dialog.DialogMassage import DialogMassage
from qss import Table


class TableNewUser(QTableWidget):
    def __init__(self, widget):
        QTableWidget.__init__(self)
        self.setStyleSheet(Table.styleDefault)
        self.widget = widget
        self.columns = widget.columns
        self.dataFrame = widget.dataFrame
        self.__setting__()
        self.__connector__()
        self.__setData__()

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)

    def __connector__(self):
        self.connDB = connDB(self.widget.windows.CURRENT_YEAR)
        self.connUser = self.connDB.connUser

    def __setData__(self):
        def btnAcceptClick():
            r = self.currentRow()
            account = self.item(r, 0).text()
            self.connUser.acceptNewUser(account)
            self.connDB.insertNewUser(account)
            self.widget.windows.RefreshNewUser()

        def btnRejectClick():
            r = self.currentRow()
            c = self.columns.index('가입승인여부')
            account = self.item(r, 0).text()
            self.connUser.rejectNewUser(account)
            i = QTableWidgetItem('거절')
            i.setFlags(Qt.ItemIsEditable)
            self.setItem(r, c, i)
            msgBox = DialogMassage('계정 정보를 삭제하시겠습니까?', True)
            if msgBox.value:
                self.connUser.deleteUser(account)
                self.widget.windows.RefreshNewUser()

        for row, lst in enumerate(self.dataFrame.values):
            self.insertRow(row)
            self.setRowHeight(row+1, 40)
            for col, data in enumerate(lst):
                item = QTableWidgetItem(data)
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(row, col, item)
            col = self.columnCount()
            BtnAcceptInTable('승인', btnAcceptClick, self, row, col-2)
            BtnRejectInTable('거절', btnRejectClick, self, row, col-1)
        self.resizeColumnsToContents()
