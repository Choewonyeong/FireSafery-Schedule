from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from material.ComboBox import CbxFilterInTable
from material.PushButton import BtnDeleteInfoInTable
from material.PushButton import BtnUpdateInfoInTable
from component.widget.WidgetHorizontalButtons import WidgetHorizontalButton
from qss import Table


class TableAdminInfo(QTableWidget):
    def __init__(self, widget):
        QTableWidget.__init__(self)
        self.setStyleSheet(Table.styleDefault)
        self.widget = widget
        self.__variables__()
        self.__setting__()
        self.__setFilter__()
        self.__setData__()

    def __variables__(self):
        self.columns = self.widget.windows.connInfo.dataFrameInfo(column=True)+['']
        self.dataFrame = self.widget.windows.connInfo.dataFrameInfo()

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)

    def __setFilter__(self):
        self.insertRow(0)
        for idx, header in enumerate(self.columns):
            if header in ['']:
                item = QTableWidgetItem('')
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(0, idx, item)
            else:
                items = self.dataFrame[header].drop_duplicates().tolist()
                if '' in items:
                    items.remove('')
                items.sort()
                items = [str(item) for item in items]
                items = ['전체']+items
                CbxFilterInTable(idx, items, self)

    def __setData__(self):
        for row, lst in enumerate(self.dataFrame.values):
            self.insertRow(row+1)
            self.setRowHeight(row+1, 40)
            for col, data in enumerate(lst):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(row+1, col, item)
            col = len(self.columns)-1
            btn1 = BtnUpdateInfoInTable('관리', self, row+1)
            btn2 = BtnDeleteInfoInTable('삭제', self, row+1)
            WidgetHorizontalButton(btn1, btn2, self, row+1, col)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setColumnWidth(2, 700)

    def Show(self):
        for row in range(1, self.rowCount()):
            self.showRow(row)

    def Filter(self, col, filterText):
        self.Show()
        for row in range(1, self.rowCount()):
            if filterText == '전체':
                pass
            elif self.item(row, col).text() != filterText:
                self.hideRow(row)
