from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from connector.connDB import connDB
from material.LineEdit import LdtTimeUserInTable


class TableTimeUser(QTableWidget):
    def __init__(self, account, year, widget):
        QTableWidget.__init__(self)
        self.account = account
        self.year = year
        self.widget = widget
        self.__connector__()
        self.__variables__()
        self.__setting__()
        self.__setData__()

    def __connector__(self):
        self.connDB = connDB(self.year)

    def __variables__(self):
        self.objects = []
        self.columns = self.connDB.dataFramePerUserTime(self.account, column=True)
        self.dataFrame = self.connDB.dataFramePerUserTime(self.account)

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
                self.setItem(row, col, item)
                obj = LdtTimeUserInTable(row, col, str(data), self)
                self.objects.append(obj)
                if col in [0, 1, 2, 3, 4, 5, 6, 7]:
                    self.hideColumn(col)
        self.resizeColumnsToContents()
