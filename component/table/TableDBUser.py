from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from connector.connDB import connDB
from material.ComboBox import CbxFilterInTable
from material.PushButton import BtnTableDBUser
from qss import Table


class TableDBUser(QTableWidget):
    def __init__(self, year, widget):
        QTableWidget.__init__(self)
        self.widget = widget
        self.setStyleSheet(Table.styleDefault)
        self.year = year
        self.__connector__()
        self.__variables__()
        self.__setting__()
        self.__setFilter__()
        self.__setData__()
        self.__setWidth__()

    def __connector__(self):
        self.connDB = connDB(self.year)
        self.connUser = self.connDB.connUser

    def __variables__(self):
        self.columns = self.connDB.dataFrameUser(column=True)
        self.columns.insert(2, '직급')
        self.columns.insert(3, '재직상태')
        self.columns[-1] = '적용상태'
        self.dataFrame = self.connDB.dataFrameUser()
        accounts = self.dataFrame['계정'].tolist()
        pos, status = self.connUser.returnSourceDB(accounts)
        self.dataFrame.insert(2, '직급', pos)
        self.dataFrame.insert(3, '재직상태', status)

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)

    def __setFilter__(self):
        self.insertRow(0)
        for idx, header in enumerate(self.columns):
            if idx == 4:
                items = ['전체'] + self.dataFrame['적용상태_부서원'].drop_duplicates().tolist()
            else:
                items = self.dataFrame[header].drop_duplicates().tolist()
                if '' in items:
                    items.remove('')
                items.sort()
                items = ['전체'] + items
            CbxFilterInTable(idx, items, self)

    def __setData__(self):
        for row, lst in enumerate(self.dataFrame.values):
            self.insertRow(row+1)
            self.setRowHeight(row+1, 40)
            for col, data in enumerate(lst):
                item = QTableWidgetItem(data)
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(row+1, col, item)
                if col != 0:
                    item.setTextAlignment(Qt.AlignCenter)
                if col == self.columnCount()-1:
                    BtnTableDBUser(data, self, row+1, col, self.year)
            self.resizeColumnsToContents()
        self.setColumnWidth(1, 65)

    def __setWidth__(self):
        width = 20
        for col in range(self.columnCount()):
            width += self.columnWidth(col)
        self.setFixedWidth(width)

    def Show(self):
        for row in range(1, self.rowCount()):
            self.showRow(row)

    def Filter(self, col, filterText):
        self.Show()
        for row in range(1, self.rowCount()):
            if self.cellWidget(0, col).currentText() == '전체':
                self.Show()
            elif self.item(row, col).text() != filterText:
                self.hideRow(row)