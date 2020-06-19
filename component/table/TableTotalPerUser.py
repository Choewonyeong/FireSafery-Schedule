from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from material.ComboBox import CbxFilterInTable
from method.totalList import returnTotalPerUser
from method.valueTran import returnTranValue
from qss import Table


class TableTotalPerUser(QTableWidget):
    def __init__(self, widget, userName):
        QTableWidget.__init__(self)
        self.setStyleSheet(Table.styleDefault)
        self.widget = widget
        self.userName = userName
        self.year = widget.windows.TOTAL_YEAR
        self.columns = widget.columns
        self.dataFrame = widget.totalDict[userName]
        self.__variables__()
        self.__setting__()
        self.__setFilter__()
        self.__setData__()

    def __variables__(self):
        self.columns = returnTotalPerUser(self.year, column=True)

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)

    def __setFilter__(self):
        self.insertRow(0)
        for idx, header in enumerate(self.columns):
            if idx == 0:
                items = self.dataFrame[header].drop_duplicates().tolist()
                if '' in items:
                    items.remove('')
                items.sort()
                items = ['전체'] + items
                CbxFilterInTable(0, items, self)
            else:
                item = QTableWidgetItem('')
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(0, idx, item)

    def __setData__(self):
        for row, lst in enumerate(self.dataFrame.values):
            self.insertRow(row+1)
            self.setRowHeight(row+1, 40)
            for col, data in enumerate(lst):
                if col != 0:
                    data = returnTranValue(data)
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row+1, col, item)
        self.resizeColumnsToContents()

    def Show(self):
        for row in range(1, self.rowCount()):
            for table in self.widget.objectTable:
                self.showRow(row)
                table.showRow(row)

    def Filter(self, col, filterText):
        self.Show()
        for row in range(1, self.rowCount()):
            if self.cellWidget(0, col).currentText() == '전체':
                for table in self.widget.objectTable:
                    self.Show()
                    table.Show()
                    table.cellWidget(0, col).setCurrentText(filterText)
            elif self.item(row, col).text() != filterText:
                for table in self.widget.objectTable:
                    self.hideRow(row)
                    table.hideRow(row)
                    table.cellWidget(0, col).setCurrentText(filterText)
