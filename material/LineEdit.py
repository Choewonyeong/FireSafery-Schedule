from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from qss import LineEdit


class LdtLogin(QLineEdit):
    def __init__(self, text=None, holderText=None):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleLogin)
        if text:
            self.setText(text)
        if holderText:
            self.setPlaceholderText(holderText)
        self.setMouseTracking(False)
        self.setAlignment(Qt.AlignCenter)


class LdtSignup(QLineEdit):
    def __init__(self, essential=False, text=None, holderText=None):
        QLineEdit.__init__(self)
        if essential:
            self.setStyleSheet(LineEdit.styleSignupEssential)
        else:
            self.setStyleSheet(LineEdit.styleSignup)
        if text:
            self.setText(text)
        if holderText:
            self.setPlaceholderText(holderText)
        self.setMouseTracking(False)
        self.setAlignment(Qt.AlignCenter)


class LdtNewBusiness(QLineEdit):
    def __init__(self, essential=False, text=None, holderText=None, enabled=True):
        QLineEdit.__init__(self)
        if essential:
            self.setStyleSheet(LineEdit.styleNewBusinessEssential)
        elif not enabled:
            self.setStyleSheet(LineEdit.styleNewBusiness)
            self.setEnabled(enabled)
        else:
            self.setStyleSheet(LineEdit.styleNewBusiness)
        if text:
            self.setText(text)
        if holderText:
            self.setPlaceholderText(holderText)
        self.setMouseTracking(False)
        self.setAlignment(Qt.AlignCenter)


class LdtNewInfo(QLineEdit):
    def __init__(self, text=None, holderText=None, enabled=True):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleNewInfo)
        self.setEnabled(enabled)
        if text:
            self.setText(text)
        if holderText:
            self.setPlaceholderText(holderText)
        self.setMouseTracking(False)
        self.setAlignment(Qt.AlignCenter)


class LdtUserSelf(QLineEdit):
    def __init__(self, lock=False, text=None, holderText=None):
        QLineEdit.__init__(self)
        if lock:
            self.setStyleSheet(LineEdit.styleSignupEssential)
        else:
            self.setStyleSheet(LineEdit.styleSignup)
        if text:
            self.setText(text)
        if holderText:
            self.setPlaceholderText(holderText)
        self.setMouseTracking(False)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedWidth(160)


class LdtDateInTable(QLineEdit):
    def __init__(self, row, col, data, table):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleInTable_Disabled)
        self.setText(str(data))
        table.setCellWidget(row, col, self)
        self.setAlignment(Qt.AlignCenter)
        self.setEnabled(False)


class LdtTimeBusinessInTable(QLineEdit):
    def __init__(self, row, col, data, table):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleInTable_default)
        self.row = row
        self.col = col
        self.init = data
        self.setText(str(data))
        self.table = table
        self.data = None
        self.editLog = False
        self.__setting__()
        self.__setStyle__()

    def __setting__(self):
        def setData(data):
            self.data = data
            if self.init == self.data:
                self.editLog = False
            elif self.init == self.data:
                self.editLog = True
        self.header = self.table.horizontalHeaderItem(self.col).text()
        self.number = self.table.item(self.row, 0).text()
        self.textChanged.connect(setData)
        self.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(self.row, self.col, self)
        self.setEnabled(False)
        if self.col in [2, 3]:
            self.setFixedWidth(80)

    def __setStyle__(self):
        count = (len(self.table.dataFrame)-3)//2
        colorRow = []
        start = 3
        colorRow.append(start)
        colorRow.append(start+1)
        for num in range(0, count):
            start += 4
            colorRow.append(start)
            colorRow.append(start+1)

        fontHideRow = [1]
        for row in range(2, len(self.table.dataFrame)+1):
            if row % 2 == 0:
                fontHideRow.append(row)

        if self.row in colorRow:
            self.setStyleSheet(LineEdit.styleInTable_background)

        if self.row in fontHideRow and self.col in [1, 2]:
            if self.row in colorRow:
                self.setStyleSheet(LineEdit.styleInTable_colorFont)
            else:
                self.setStyleSheet(LineEdit.styleInTable_whiteFont)


class LdtTimeUserInTable(QLineEdit):
    def __init__(self, row, col, data, table):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleInTable_default)
        self.row = row
        self.col = col
        self.init = data
        self.setText(str(data))
        self.table = table
        self.data = None
        self.editLog = False
        self.__setting__()
        self.__setStyle__()

    def __setting__(self):
        def setData(data):
            self.data = data
            if self.init == self.data:
                self.editLog = False
            else:
                self.editLog = True
        self.header = self.table.horizontalHeaderItem(self.col).text()
        self.number = self.table.item(self.row, 0).text()
        self.textChanged.connect(setData)
        self.textChanged.connect(self.table.widget.changeTotalValue)
        self.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(self.row, self.col, self)
        self.setFixedWidth(60)

    def __setStyle__(self):
        count = (len(self.table.dataFrame)-3)//2
        colorRow = []
        start = 3
        colorRow.append(start)
        colorRow.append(start+1)
        for num in range(0, count):
            start += 4
            colorRow.append(start)
            colorRow.append(start+1)

        fontHideRow = []
        for row in range(2, len(self.table.dataFrame)+1):
            if row % 2 == 0:
                fontHideRow.append(row)

        if self.row in colorRow:
            self.setStyleSheet(LineEdit.styleInTable_background)


class LdtTimeDayTotalInTable(QLineEdit):
    def __init__(self, row, col, data, table):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleInTable_total)
        self.row = row
        self.col = col
        self.init = data
        self.setText(str(data))
        self.table = table
        self.__setting__()

    def __setting__(self):
        self.header = self.table.horizontalHeaderItem(self.col).text()
        self.number = self.table.item(self.row, 0).text()
        self.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(self.row, self.col, self)
        self.setFixedWidth(60)
        self.setEnabled(False)


class LdtAdminUserInTable(QLineEdit):
    def __init__(self, row, col, data, table):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleInTable_default)
        self.row = row
        self.col = col
        self.init = data
        self.setText(str(data))
        self.table = table
        self.header = table.horizontalHeaderItem(col).text()
        self.number = table.item(row, 0).text()
        self.data = None
        self.editLog = False
        table.setCellWidget(row, col, self)
        self.__setting__()

    def __setting__(self):
        def setData(data):
            self.data = data
            if self.init == self.data:
                self.editLog = False
            else:
                self.editLog = True
        self.textChanged.connect(setData)
        self.setAlignment(Qt.AlignCenter)


class LdtAdminBusinessInTable(QLineEdit):
    def __init__(self, row, col, data, table):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleInTable_default)
        self.row = row
        self.col = col
        self.init = data
        self.setText(str(data))
        self.table = table
        self.header = table.horizontalHeaderItem(col).text()
        self.number = table.item(row, 0).text()
        self.data = None
        self.editLog = False
        table.setCellWidget(row, col, self)
        self.__setting__()

    def __setting__(self):
        def setData(data):
            self.data = data
            if self.init == self.data:
                self.editLog = False
            else:
                self.editLog = True
        self.textChanged.connect(setData)
        if self.col != 1:
            self.setAlignment(Qt.AlignCenter)


class LdtEditPasswordLeft(QLineEdit):
    def __init__(self, text=None, holderText=None):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleEditPassword_left)
        self.setEchoMode(QLineEdit.Password)
        if text:
            self.setText(text)
        if holderText:
            self.setPlaceholderText(holderText)
        self.setMouseTracking(False)
        self.setAlignment(Qt.AlignCenter)


class LdtEditPasswordRight(QLineEdit):
    def __init__(self, text=None, holderText=None):
        QLineEdit.__init__(self)
        self.setStyleSheet(LineEdit.styleEditPassword_right)
        self.setEchoMode(QLineEdit.Password)
        if text:
            self.setText(text)
        if holderText:
            self.setPlaceholderText(holderText)
        self.setMouseTracking(False)
        self.setAlignment(Qt.AlignCenter)
