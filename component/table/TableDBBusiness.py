from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from connector.connDB import connDB
from material.ComboBox import CbxFilterInTable
from material.PushButton import BtnTableDBBusiness
from qss import Table


class TableDBBusiness(QTableWidget):
    def __init__(self, year, widget):
        QTableWidget.__init__(self)
        self.setStyleSheet(Table.styleDefault)
        self.widget = widget
        self.year = year
        self.__connector__()
        self.__variables__()
        self.__setting__()
        self.__setFilter__()
        self.__setData__()
        self.__setWidth__()

    def __connector__(self):
        self.connDB = connDB(self.year)
        self.connBusiness = self.connDB.connBusiness

    def __variables__(self):
        self.columns = self.connDB.dataFrameBusiness(column=True)
        self.columns.insert(3, '사업형태')
        self.columns.insert(4, '시작일')
        self.columns.insert(5, '종료일')
        self.columns.insert(6, '진행상태')
        self.columns[-1] = '적용상태'
        self.dataFrame = self.connDB.dataFrameBusiness()
        numbers = self.dataFrame['번호'].tolist()
        form, start, end, status = self.connBusiness.returnSourceDB(numbers)
        self.dataFrame.insert(3, '사업형태', form)
        self.dataFrame.insert(4, '시작일', start)
        self.dataFrame.insert(5, '종료일', end)
        self.dataFrame.insert(6, '진행상태', status)
        self.dataFrame = self.dataFrame.reset_index(drop=True)
        self.dataFrame = self.dataFrame.drop(len(self.dataFrame)-1)
        self.dataFrame = self.dataFrame.drop(0)

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)

    def __setFilter__(self):
        self.insertRow(0)
        for idx, header in enumerate(self.columns):
            if idx == 0:
                item = QTableWidgetItem('')
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(0, idx, item)
            elif idx == 7:
                items = ['전체'] + self.dataFrame['적용상태_사업'].drop_duplicates().tolist()
                CbxFilterInTable(idx, items, self)
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
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(row+1, col, item)
                if col != 1:
                    item.setTextAlignment(Qt.AlignCenter)
                if col == self.columnCount()-1:
                    BtnTableDBBusiness(data, self, row+1, col, self.year)
            self.resizeColumnsToContents()
            self.hideColumn(0)
        self.setColumnWidth(2, 65)
        self.setColumnWidth(4, 120)
        self.setColumnWidth(5, 120)

    def __setWidth__(self):
        width = 20
        for col in range(1, self.columnCount()):
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



