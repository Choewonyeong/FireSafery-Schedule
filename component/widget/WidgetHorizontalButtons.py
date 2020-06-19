from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout


class WidgetHorizontalButton(QWidget):
    def __init__(self, btn1, btn2, table, row, col):
        QWidget.__init__(self)
        self.btn1 = btn1
        self.btn2 = btn2
        self.table = table
        self.__layout__()
        self.__setWidth__()
        table.setCellWidget(row, col, self)

    def __layout__(self):
        layout = QHBoxLayout()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        self.setLayout(layout)

    def __setWidth__(self):
        width = 20
        width += self.btn1.width()
        width += self.btn2.width()
        self.setFixedWidth(width)
