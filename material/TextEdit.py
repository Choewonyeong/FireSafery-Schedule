from PyQt5.QtWidgets import QTextEdit
from qss.TextEdit import styleInfo


class TdtInfo(QTextEdit):
    def __init__(self, text=''):
        QTextEdit.__init__(self)
        self.setStyleSheet(styleInfo)
        self.setText(text)

