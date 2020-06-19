from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from connector.connDB import connDB
from material.LineEdit import LdtTimeDayTotalInTable


class TableTimeTotal(QTableWidget):
    def __init__(self, account, year, columns):
        QTableWidget.__init__(self)
        self.account = account
        self.year = year
        self.columns = columns
        self.__connector__()
        self.__variables__()
        self.__setting__()
        self.__setData__()

    def __connector__(self):
        self.connDB = connDB(self.year)

    def __variables__(self):
        self.lst = self.connDB.listTotal(self.columns, self.account)

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __setData__(self):
        self.insertRow(0)
        for col, data in enumerate(self.lst):
            split = str(data).split('.')
            intValue = int(split[1])
            if data == 0.0:
                data = ''
            elif intValue == 0:
                data = str(int(data))
            else:
                data = str(data)
            item = QTableWidgetItem(data)
            item.setFlags(Qt.ItemIsEditable)
            self.setItem(0, col, item)
            LdtTimeDayTotalInTable(0, col, str(data), self)
        self.resizeColumnsToContents()

