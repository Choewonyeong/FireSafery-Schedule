from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QEvent
from qss import PushButton


class BtnLogin(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleLogin)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnClose(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleClose)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnSignup(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleSignUp)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnOk(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleYes)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnNo(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleNo)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnYes(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleYes)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnSubmit(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleSubmit)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnCancel(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleCancel)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnUserSelfSave(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleUserSelf_Save)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnUserSelfClose(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleUserSelf_Close)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnUserTimeClose(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleDefault)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnTabClose(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleDefault)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        self.setCursor(Qt.PointingHandCursor)
        if shortcut:
            self.setShortcut(shortcut)


class BtnTool(QPushButton):
    def __init__(self, text, event, default=False, shortcut=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleDefault)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        self.setDefault(default)
        if shortcut:
            self.setShortcut(shortcut)


class BtnAcceptInTable(QPushButton):
    def __init__(self, text, event, table, row, col):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleInTable_Accept)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        table.setCellWidget(row, col, self)


class BtnRejectInTable(QPushButton):
    def __init__(self, text, event, table, row, col):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleInTable_Accept)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(event)
        table.setCellWidget(row, col, self)


class BtnPasswordInTable(QPushButton):
    def __init__(self, text, table, row, col):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleInTable_Default)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.table = table
        self.row = row
        self.col = col
        self.setFixedWidth(80)
        self.clicked.connect(self.btnClick)
        table.setCellWidget(row, col, self)
        self.account = self.table.item(self.row, 0).text()

    def btnClick(self):
        from component.dialog.DialogAdmin import DialogAdmin
        DialogAdmin(self.account, self.row, self.table)


class BtnDeleteBusinessInTable(QPushButton):
    def __init__(self, text, table, row, col):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleInTable_Default)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.table = table
        self.row = row
        self.col = col
        self.setFixedWidth(80)
        self.clicked.connect(self.btnClick)
        table.setCellWidget(row, col, self)
        self.number = self.table.item(self.row, 0).text()

    def btnClick(self):
        from component.dialog.DialogMassage import DialogMassage
        question = DialogMassage('사업 정보를 삭제하시겠습니까?\n삭제 시 해당 사업에 대한 모든 정보가 삭제되며\n삭제 후에는 되돌릴 수 없습니다.', question=True)
        if question.value:
            from connector.connDB import connDB
            from connector.connDB import connBusiness
            __connDB__ = connDB(self.table.widget.windows.CURRENT_YEAR)
            __connDB__.deleteBusiness(self.number)
            __connUser__ = connBusiness()
            __connUser__.deleteBusiness(self.number)
            DialogMassage('사업 정보가 삭제되었습니다.')
            self.table.widget.windows.RefreshAdminBusiness()


class BtnDeleteUserInTable(QPushButton):
    def __init__(self, text, table, row, col):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleInTable_Default)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.table = table
        self.row = row
        self.col = col
        self.setFixedWidth(80)
        self.clicked.connect(self.btnClick)
        table.setCellWidget(row, col, self)
        self.account = self.table.item(self.row, 0).text()

    def btnClick(self):
        from component.dialog.DialogMassage import DialogMassage
        question = DialogMassage('계정 정보를 삭제하시겠습니까?\n삭제 시 해당 계정에 대한 모든 정보가 삭제되며\n삭제 후에는 되돌릴 수 없습니다.', question=True)
        if question.value:
            from connector.connDB import connDB
            from connector.connDB import connUser
            __connDB__ = connDB(self.table.widget.windows.CURRENT_YEAR)
            __connDB__.deleteUser(self.account)
            __connUser__ = connUser()
            __connUser__.deleteUser(self.account)
            DialogMassage('계정 정보가 삭제되었습니다.')
            self.table.widget.windows.RefreshAdminUser()


class BtnTableDBUser(QPushButton):
    def __init__(self, text, table, row, col, year):
        QPushButton.__init__(self)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        if text == '적용':
            self.setStyleSheet(PushButton.styleInTable_Apply)
        elif text == '제외':
            self.setStyleSheet(PushButton.styleInTable_Except)
        self.table = table
        self.row = row
        self.col = col
        self.year = year
        self.clicked.connect(self.btnClick)
        self.account = table.item(self.row, 0).text()
        table.setCellWidget(row, col, self)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter and self.text() == '적용':
            self.setText('제외')
            self.setStyleSheet(PushButton.styleInTable_Except)
        elif event.type() == QEvent.Enter and self.text() == '제외':
            self.setText('적용')
            self.setStyleSheet(PushButton.styleInTable_Apply)
        elif event.type() == QEvent.Leave and self.text() == '적용':
            self.setText('제외')
            self.setStyleSheet(PushButton.styleInTable_Except)
        elif event.type() == QEvent.Leave and self.text() == '제외':
            self.setText('적용')
            self.setStyleSheet(PushButton.styleInTable_Apply)
        return False

    def btnClick(self):
        from component.dialog.DialogMassage import DialogMassage
        if self.text() == '제외':
            msgBox = DialogMassage("해당 계정을 현재의 데이터베이스에서 제외하시겠습니까?", True)
            if msgBox.value:
                from connector.connDB import connDB
                __connDB__ = connDB(self.year)
                __connDB__.updateUserApplyStatus('제외', self.account)
        elif self.text() == '적용':
            msgBox = DialogMassage("해당 계정을 현재의 데이터베이스에 적용시키겠습니까?", True)
            if msgBox.value:
                from connector.connDB import connDB
                __connDB__ = connDB(self.year)
                __connDB__.updateUserApplyStatus('적용', self.account)
        self.table.widget.windows.RefreshAdminDB()


class BtnTableDBBusiness(QPushButton):
    def __init__(self, text, table, row, col, year):
        QPushButton.__init__(self)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        if text == '적용':
            self.setStyleSheet(PushButton.styleInTable_Apply)
        elif text == '제외':
            self.setStyleSheet(PushButton.styleInTable_Except)
        self.table = table
        self.row = row
        self.year = year
        self.clicked.connect(self.btnClick)
        self.number = table.item(self.row, 0).text()
        table.setCellWidget(row, col, self)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter and self.text() == '적용':
            self.setText('제외')
            self.setStyleSheet(PushButton.styleInTable_Except)
        elif event.type() == QEvent.Enter and self.text() == '제외':
            self.setText('적용')
            self.setStyleSheet(PushButton.styleInTable_Apply)
        elif event.type() == QEvent.Leave and self.text() == '적용':
            self.setText('제외')
            self.setStyleSheet(PushButton.styleInTable_Except)
        elif event.type() == QEvent.Leave and self.text() == '제외':
            self.setText('적용')
            self.setStyleSheet(PushButton.styleInTable_Apply)
        return False

    def btnClick(self):
        from component.dialog.DialogMassage import DialogMassage
        if self.text() == '제외':
            msgBox = DialogMassage("해당 사업을 현재의 데이터베이스에서 제외하시겠습니까?", True)
            if msgBox.value:
                from connector.connDB import connDB
                __connDB__ = connDB(self.year)
                __connDB__.updateBusinessApplyStatus('제외', self.number)
        elif self.text() == '적용':
            msgBox = DialogMassage("해당 사업을 현재의 데이터베이스에 적용시키겠습니까?", True)
            if msgBox.value:
                from connector.connDB import connDB
                __connDB__ = connDB(self.year)
                __connDB__.updateBusinessApplyStatus('적용', self.number)
        self.table.widget.windows.RefreshAdminDB()


class BtnCreateNewDB(QPushButton):
    def __init__(self, text, shortcut='', windows=None):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleInTable_Default)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(self.btnClick)
        if shortcut:
            self.setShortcut(shortcut)
        self.windows = windows

    def btnClick(self):
        from component.dialog.DialogMassage import DialogMassage
        from connector.connDB import connDB
        nextYear = self.text()[:4]
        question = DialogMassage(f"{nextYear}년 데이터베이스를 생성하시겠습니까?", question=True)
        if question.value:
            conn = connDB(nextYear)
            conn.createDB()
            self.windows.RefreshAdminDB()


class BtnUpdateInfoInTable(QPushButton):
    def __init__(self, text, table, row):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleInTable_Default)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.row = row
        self.table = table
        self.setFixedWidth(80)
        self.clicked.connect(self.btnClick)

    def btnClick(self):
        from component.dialog.DialogEditInfo import DialogEditInfo
        DialogEditInfo(self.table.widget.windows, self.table, self.row)


class BtnDeleteInfoInTable(QPushButton):
    def __init__(self, text, table, row):
        QPushButton.__init__(self)
        self.setStyleSheet(PushButton.styleInTable_Default)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(text)
        self.table = table
        self.setFixedWidth(80)
        self.clicked.connect(self.btnClick)
        self.number = self.table.item(row, 0).text()

    def btnClick(self):
        from component.dialog.DialogMassage import DialogMassage
        from connector.connInfo import connInfo
        question = DialogMassage('알림 정보를 삭제하시겠습니까?', question=True)
        if question.value:
            from connector.connDB import connDB
            from connector.connDB import connUser
            __connInfo__ = connInfo()
            __connInfo__.deleteInfo(self.number)
            self.table.widget.windows.RefreshAdminInfo()
            DialogMassage('알림 정보가 삭제되었습니다.')

