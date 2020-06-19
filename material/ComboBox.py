from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from qss import ComboBox


class CbxSignup(QComboBox):
    def __init__(self, items, text=None):
        QComboBox.__init__(self)
        self.setStyleSheet(ComboBox.styleSignup)
        self.addItems(items)
        if text:
            self.setCurrentText(text)
        self.setCursor(Qt.PointingHandCursor)


class CbxNewBusiness(QComboBox):
    def __init__(self, items, text=None):
        QComboBox.__init__(self)
        self.setStyleSheet(ComboBox.styleNewBusiness)
        self.addItems(items)
        if text:
            self.setCurrentText(text)
        self.setCursor(Qt.PointingHandCursor)


class CbxNewInfo(QComboBox):
    def __init__(self, items, text=None):
        QComboBox.__init__(self)
        self.setStyleSheet(ComboBox.styleNewInfo)
        self.addItems(items)
        if text:
            self.setCurrentText(text)
        self.setCursor(Qt.PointingHandCursor)


class CbxNewInfo_Date(QComboBox):
    def __init__(self, items, text=None):
        QComboBox.__init__(self)
        self.setStyleSheet(ComboBox.styleNewInfo_Date)
        self.addItems(items)
        if text:
            self.setCurrentText(text)
        self.setCursor(Qt.PointingHandCursor)


class CbxUserSelf(QComboBox):
    def __init__(self, items, text=None):
        QComboBox.__init__(self)
        self.setStyleSheet(ComboBox.styleUserSelf)
        self.addItems(items)
        if text:
            self.setCurrentText(text)
        self.setCursor(Qt.PointingHandCursor)


class CbxFilterInTable(QComboBox):
    def __init__(self, col, items, table):
        QComboBox.__init__(self)
        self.setStyleSheet(ComboBox.styleFilter)
        self.col = col
        self.addItems(items)
        self.table = table
        table.setCellWidget(0, col, self)
        self.setCursor(Qt.PointingHandCursor)
        self.__setEvent__()

    def __setEvent__(self):
        def textChange(text):
            self.table.Filter(self.col, text)
        self.currentTextChanged.connect(textChange)


class CbxYears(QComboBox):
    def __init__(self, items, text=None):
        QComboBox.__init__(self)
        self.setStyleSheet(ComboBox.styleYear)
        self.addItems(items)
        if text:
            self.setCurrentText(text)
        self.setCursor(Qt.PointingHandCursor)


class CbxToolInTable(QComboBox):
    def __init__(self, row, col, items, data, table):
        QComboBox.__init__(self)
        self.setStyleSheet(ComboBox.styleInTable)
        self.row = row
        self.col = col
        self.addItems(items)
        self.init = ''
        if data:
            self.setCurrentText(data)
            self.init = data
        self.editLog = False
        self.table = table
        self.header = table.horizontalHeaderItem(col).text()
        self.number = table.item(row, 0).text()
        table.setCellWidget(row, col, self)
        self.setCursor(Qt.PointingHandCursor)
        self.__setEvent__()

    def __setEvent__(self):
        def setData(data):
            self.data = data
            if self.init == self.data:
                self.editLog = False
            elif self.init != self.data:
                self.editLog = True
        self.currentTextChanged.connect(setData)
