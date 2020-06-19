from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from material.Label import LblDash
from material.Label import LblNull
from qss import GroupBox


class GbxSignup(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self)
        self.setStyleSheet(GroupBox.styleDefault)


class GbxSelectDateTime(QGroupBox):
    def __init__(self, windows, year=None, month=None, day=None):
        from material.ComboBox import CbxNewInfo_Date
        from datetime import datetime
        from pandas import Timedelta
        QGroupBox.__init__(self)
        self.setStyleSheet(GroupBox.styleDefault)
        self.cbxYear = CbxNewInfo_Date(items=[f"{int(windows.CURRENT_YEAR)+cnt}" for cnt in range(5)])
        self.cbxMonth = CbxNewInfo_Date(items=[f"0{month}" if month < 10 else f"{month}" for month in range(1, 13)])
        self.cbxMonth.setCurrentText(datetime.today().strftime("%m"))
        currentEndMonth = datetime(int(self.cbxYear.currentText()), int(self.cbxMonth.currentText()), 1, 0, 0, 0)
        nextEndMonth = datetime(int(self.cbxYear.currentText()), int(self.cbxMonth.currentText()) + 1, 1, 0, 0, 0)
        dayCount = Timedelta(nextEndMonth - currentEndMonth).days
        self.cbxDay = CbxNewInfo_Date(items=[f"0{day}" if day < 10 else f"{day}" for day in range(1, dayCount+1)])
        self.cbxDay.setCurrentText(datetime.today().strftime("%d"))
        if year:
            self.cbxYear.setCurrentText(year)
        if month:
            self.cbxMonth.setCurrentText(month)
        if day:
            self.cbxDay.setCurrentText(day)
        self.year = self.cbxYear.currentText()
        self.month = self.cbxMonth.currentText()
        self.day = self.cbxDay.currentText()
        self.date = f"{self.year}-{self.month}-{self.day}"
        self.__setEvent__()
        self.__layout__()

    def __setEvent__(self):
        from datetime import datetime
        from pandas import Timedelta

        def yearChanged(year):
            self.year = year
            self.date = f"{self.year}-{self.month}-{self.day}"
            self.cbxMonth.setCurrentIndex(0)
        self.cbxYear.currentTextChanged.connect(yearChanged)

        def monthChanged(month):
            self.month = month
            self.date = f"{self.year}-{self.month}-{self.day}"
            year = int(self.cbxYear.currentText())
            month = int(month)
            startMonth = datetime(year, month, 1, 0, 0, 0)
            nextMonth = datetime(year, month + 1, 1, 0, 0, 0)
            count = Timedelta(nextMonth - startMonth).days
            self.cbxDay.clear()
            self.cbxDay.addItems([f"0{day}" if day < 10 else f"{day}" for day in range(1, count+1)])
        self.cbxMonth.currentTextChanged.connect(monthChanged)

        def dayChanged(day):
            self.day = day
            self.date = f"{self.year}-{self.month}-{self.day}"
        self.cbxDay.currentTextChanged.connect(dayChanged)

    def __layout__(self):
        layout = QHBoxLayout()
        layout.addWidget(self.cbxYear)
        layout.addWidget(LblDash())
        layout.addWidget(self.cbxMonth)
        layout.addWidget(LblDash())
        layout.addWidget(self.cbxDay)
        layout.addWidget(LblNull(), 10)
        self.setLayout(layout)
