from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget
from qss import ListWidget


class LstMain(QListWidget):
    def __init__(self, items, itemEvent):
        QListWidget.__init__(self)
        self.setStyleSheet(ListWidget.styleMain)
        self.addItems(items)
        self.setFixedWidth(120)
        self.itemClicked.connect(itemEvent)
        self.setCursor(Qt.PointingHandCursor)


class LstSub(QListWidget):
    def __init__(self, items, itemEvent):
        QListWidget.__init__(self)
        self.setStyleSheet(ListWidget.styleSub)
        self.addItems(items)
        self.setFixedWidth(120)
        self.setVisible(False)
        self.itemClicked.connect(itemEvent)
        self.setCursor(Qt.PointingHandCursor)
