from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import setting


class Loading(QSplashScreen):
    def __init__(self):
        QSplashScreen.__init__(self)
        self.setPixmap(QPixmap(setting.imgLogo).scaledToWidth(500))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.mousePressEvent = self.MousePressEvent
        self.keyPressEvent = self.KeyPressEvent
        self.show()

    def MousePressEvent(self, e):
        pass

    def KeyPressEvent(self, e):
        pass