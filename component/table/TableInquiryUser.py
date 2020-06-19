from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from material.ComboBox import CbxFilterInTable
from qss import Table


class TableInquiryUser(QTableWidget):
    def __init__(self, widget):
        QTableWidget.__init__(self)
        self.setStyleSheet(Table.styleDefault)
        self.widget = widget
        self.__variables__()
        self.__setting__()
        self.__setFilter__()
        self.__setData__()

    def __variables__(self):
        self.columns = self.widget.windows.connUser.dataFrameUser(column=True)
        self.dataFrame = self.widget.windows.connUser.dataFrameUser()
        for col in [14, 13, 12, 2]:
            self.dataFrame = self.dataFrame.drop(self.dataFrame.columns[col], axis='columns')
            self.columns.pop(col)

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)

    def __setFilter__(self):
        self.insertRow(0)
        for idx, header in enumerate(self.columns):
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
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(row+1, col, item)
        self.resizeColumnsToContents()
        self.setColumnWidth(1, 65)
        self.setColumnWidth(4, 110)

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
