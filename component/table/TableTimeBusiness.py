from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from connector.connDB import connDB
from material.LineEdit import LdtTimeBusinessInTable


class TableTimeBusiness(QTableWidget):
    def __init__(self, account, year):
        QTableWidget.__init__(self)
        self.account = account
        self.year = year
        self.__connector__()
        self.__variables__()
        self.__setting__()
        self.__setData__()
        self.__setWidth__()

    def __connector__(self):
        self.connDB = connDB(self.year)

    def __variables__(self):
        self.columns = self.connDB.dataFramePerUserBusiness(self.account, column=True)
        self.dataFrame = self.connDB.dataFramePerUserBusiness(self.account)

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __setData__(self):
        for row, lst in enumerate(self.dataFrame.values):
            self.insertRow(row)
            for col, data in enumerate(lst):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(row, col, item)
                LdtTimeBusinessInTable(row, col, data, self)
                if col == 0:
                    self.hideColumn(col)
        self.resizeColumnsToContents()

    def __setWidth__(self):
        self.width = 0
        for col in range(1, self.columnCount()):
            self.width += self.columnWidth(col)
        self.setFixedWidth(self.width)

    def refresh(self):
        self.clear()
        self.__connector__()
        self.__variables__()
        self.__setting__()
        self.__setData__()
        self.__setWidth__()
