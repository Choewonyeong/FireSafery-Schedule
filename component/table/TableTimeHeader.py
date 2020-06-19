from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from qss import Table


class TableTimeHeader(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)
        self.setStyleSheet(Table.styleTitle)
        self.__setting__()
        self.__setData__()

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels([''])
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __setData__(self):
        self.insertRow(0)
        item = QTableWidgetItem('일간합계')
        item.setFlags(Qt.ItemIsEditable)
        item.setTextAlignment(Qt.AlignCenter)
        self.setItem(0, 0, item)
