from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from connector.connUser import connUser
from material.Label import LblImage
from material.Label import LblNull
from material.LineEdit import LdtLogin
from material.PushButton import BtnLogin
from material.PushButton import BtnClose
from material.PushButton import BtnSignup
from qss.Dialog import styleLogin
from component.dialog.DialogMassage import DialogMassage
import setting


class Login(QDialog):
    def __init__(self, app):
        QDialog.__init__(self)
        self.app = app
        self.setStyleSheet(styleLogin)
        self.__setting__()
        self.__connector__()
        self.__variables__()
        self.__component__()

    def __setting__(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(400)
        self.setFixedHeight(600)

    def __connector__(self):
        self.connUser = connUser()

    def __variables__(self):
        self.account = ''
        self.author = ''
        self.accounts = self.connUser.returnAccounts()
        self.stanByAccounts = self.connUser.returnStanByAccounts()

    def __component__(self):
        self.__label__()
        self.__lineEdit__()
        self.__pushButton__()
        self.__layout__()

    def __label__(self):
        self.lblImg = LblImage(setting.imgLogin, 125)
        self.lblLogo = LblImage(setting.imgLogo, 200)

    def __lineEdit__(self):
        self.ldtAccount = LdtLogin('', 'Account')
        self.ldtPassword = LdtLogin('', 'Password')
        self.ldtPassword.setEchoMode(LdtLogin.Password)

    def __pushButton__(self):
        def btnCloseClick():
            self.app.quit()

        def btnLoginClick():
            account = self.ldtAccount.text()
            password = self.ldtPassword.text()
            if account == '':
                DialogMassage('계정을 입력하세요.')
            elif account in self.stanByAccounts:
                admins = self.connUser.returnAdmins()
                DialogMassage(f"가입 승인 대기 중인 계정입니다.\n관리자에게 승인을 요청하세요.\n\n○ 관리자 : {', '.join(admins)}")
            elif account not in self.accounts + self.stanByAccounts:
                DialogMassage('등록되지 않은 계정입니다.')
            elif password == '':
                DialogMassage('비밀번호를 입력하세요.')
            elif password != self.connUser.returnPassword(account):
                DialogMassage('비밀번호가 일치하지 않습니다.')
                self.ldtPassword.setText('')
            elif account in self.stanByAccounts:
                admins = self.connUser.returnAdmins().pop(0)
                DialogMassage(f"가입 승인 대기 중인 계정입니다.\n관리자에게 승인을 요청하세요.\n\n○ 관리자 : {', '.join(admins)}")
            else:
                from component.main.Windows import Windows
                author = self.connUser.returnAuthor(account)
                windows = Windows(account, author, self.app, self)
                windows.show()
                self.close()
                self.app.exec_()

        def btnSignupClick():
            from component.dialog.DialogSignup import Signup
            signup = Signup()
            signup.exec_()

        self.btnClose = BtnClose('닫기', btnCloseClick)
        self.btnClose.setCursor(Qt.PointingHandCursor)
        self.btnClose.clicked.connect(btnCloseClick)
        self.btnLogin = BtnLogin('로그인', btnLoginClick, default=True, shortcut='return')
        self.btnSignup = BtnSignup('회원가입', btnSignupClick)

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnLogin)
        layout = QVBoxLayout()
        layout.addWidget(LblNull())
        layout.addWidget(self.lblImg)
        layout.addWidget(self.ldtAccount)
        layout.addWidget(self.ldtPassword)
        layout.addLayout(layoutBtn)
        layout.addWidget(self.btnSignup)
        layout.addWidget(LblNull())
        layout.addWidget(self.lblLogo)
        self.setLayout(layout)
