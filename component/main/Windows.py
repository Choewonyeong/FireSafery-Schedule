from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QHBoxLayout
from connector.connBusiness import connBusiness
from connector.connUser import connUser
from connector.connInfo import connInfo
from material.ListWidget import LstMain
from material.ListWidget import LstSub
from component.dialog.DialogInfo import DialogInfo
from component.dialog.DialogUserSelf import DialogUserSelf
from component.dialog.DialogMassage import DialogMassage
from component.main.MainUserTime import MainUserTime
from component.main.MainAdminBusiness import MainAdminBusiness
from component.main.MainAdminUser import MainAdminUser
from component.main.MainInquiryUser import MainInquiryUser
from component.main.MainNewUser import MainNewUser
from component.main.MainDatabase import MainDatabase
from component.main.MainTotalPerYear import MainTotalPerYear
from component.main.MainTotalPerUser import MainTotalPerUser
from component.main.MainAdminInfo import MainAdminInfo
from datetime import datetime
import setting


class Windows(QWidget):
    CURRENT_YEAR = str(datetime.today().year)
    TIME_YEAR = str(datetime.today().year)
    DB_YEAR = str(datetime.today().year)
    TOTAL_YEAR = str(datetime.today().year)

    def __init__(self, account, author, app, dig):
        QWidget.__init__(self)
        self.account = account
        self.author = author
        self.app = app
        self.dig = dig
        self.closeEvent = self.closeQuestion
        self.__setting__()
        self.__connector__()
        self.__variables__()
        self.__component__()

    def __setting__(self):
        self.setWindowTitle('화재안전팀 시간관리 프로그램 - (주)스탠더드시험연구소')
        self.setWindowIcon(QIcon(setting.iconIcon))
        self.showMaximized()
        background = QPalette()
        background.setBrush(10, QBrush(QColor(255, 255, 255)))
        self.setPalette(background)

    def __connector__(self):
        self.connUser = connUser()
        self.connBusiness = connBusiness()
        self.connInfo = connInfo()

    def __variables__(self):
        self.lstMainIterator = []
        self.name = self.connUser.returnName(self.account)
        self.itemMain = [self.name, '조회', '관리', '로그아웃']
        if self.author != "관리자":
            self.itemMain.remove('관리')
        self.itemUser = ['개인정보', '시간관리']
        self.itemInquiry = ['부서원 정보 조회', '연도별시간집계', '부서원별시간집계']
        self.itemAdmin = ['회원가입 신청 현황', '부서원 정보 관리', '사업 정보 관리', '데이터베이스 관리', '공지사항 관리']
        self.valueUser = False
        self.valueInquiry = False
        self.valueAdmin = False
        self.currentTabs = []

    def __component__(self):
        self.__listWidget__()
        self.__tab__()
        self.__layout__()
        self.__info__()
        self.__ObjectRefresh__()

    def __listWidget__(self):
        def lstMainItemClick(item):
            menu = item.text()
            if menu == self.name and not self.valueUser:
                self.lstUser.setVisible(True)
                self.lstInquiry.setVisible(False)
                self.lstAdmin.setVisible(False)
                self.valueUser = True
                self.valueInquiry = False
                self.valueAdmin = False
            elif menu == '조회' and not self.valueInquiry:
                self.lstUser.setVisible(False)
                self.lstInquiry.setVisible(True)
                self.lstAdmin.setVisible(False)
                self.valueUser = False
                self.valueInquiry = True
                self.valueAdmin = False
            elif menu == '관리' and not self.valueAdmin:
                self.lstUser.setVisible(False)
                self.lstInquiry.setVisible(False)
                self.lstAdmin.setVisible(True)
                self.valueUser = False
                self.valueInquiry = False
                self.valueAdmin = True
            elif menu == '로그아웃':
                mgs = DialogMassage('로그아웃을 진행합니까?\n저장하지 않은 정보가 있는지 확인바랍니다.', True)
                if mgs.value:
                    self.closeEvent = self.closePass
                    self.close()
                    self.dig.exec_()
            else:
                self.lstUser.setVisible(False)
                self.lstInquiry.setVisible(False)
                self.lstAdmin.setVisible(False)
                self.valueUser = False
                self.valueInquiry = False
                self.valueAdmin = False
        self.lstMain = LstMain(self.itemMain, lstMainItemClick)

        def lstUserItemClick(item):
            menu = item.text()
            if menu == self.itemUser[0]:
                DialogUserSelf(self.account, self)
            elif menu == self.itemUser[1] and menu not in self.currentTabs:
                self.tab.addTab(MainUserTime(self), menu)
                self.currentTabs.append(menu)
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
            else:
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
                self.refreshUser[menu]()
        self.lstUser = LstSub(self.itemUser, lstUserItemClick)

        def lstInquiryItemClick(item):
            menu = item.text()
            if menu == self.itemInquiry[0] and menu not in self.currentTabs:
                self.tab.addTab(MainInquiryUser(self), menu)
                self.currentTabs.append(menu)
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
            elif menu == self.itemInquiry[1] and menu not in self.currentTabs:
                self.tab.addTab(MainTotalPerYear(self), menu)
                self.currentTabs.append(menu)
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
            elif menu == self.itemInquiry[2] and menu not in self.currentTabs:
                self.tab.addTab(MainTotalPerUser(self), menu)
                self.currentTabs.append(menu)
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
            else:
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
                self.refreshInquiry[menu]()
        self.lstInquiry = LstSub(self.itemInquiry, lstInquiryItemClick)

        def lstAdminItemClick(item):
            menu = item.text()
            if menu == self.itemAdmin[0] and menu not in self.currentTabs:
                widget = MainNewUser(self)
                if len(widget.tblNewUser.dataFrame):
                    self.tab.addTab(widget, menu)
                    self.currentTabs.append(menu)
                    self.tab.setCurrentIndex(self.currentTabs.index(menu))
                else:
                    DialogMassage('신청 대상이 없습니다.')
            elif menu == self.itemAdmin[1] and menu not in self.currentTabs:
                self.tab.addTab(MainAdminUser(self), menu)
                self.currentTabs.append(menu)
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
            elif menu == self.itemAdmin[2] and menu not in self.currentTabs:
                self.tab.addTab(MainAdminBusiness(self), menu)
                self.currentTabs.append(menu)
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
            elif menu == self.itemAdmin[3] and menu not in self.currentTabs:
                self.tab.addTab(MainDatabase(self), menu)
                self.currentTabs.append(menu)
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
            elif menu == self.itemAdmin[4] and menu not in self.currentTabs:
                self.tab.addTab(MainAdminInfo(self), menu)
                self.currentTabs.append(menu)
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
            else:
                self.tab.setCurrentIndex(self.currentTabs.index(menu))
                self.refreshAdmin[menu]()
        self.lstAdmin = LstSub(self.itemAdmin, lstAdminItemClick)

    def __tab__(self):
        self.tab = QTabWidget()
        self.tab.tabBar().setVisible(False)

    def __layout__(self):
        layout = QHBoxLayout()
        layout.addWidget(self.lstMain)
        layout.addWidget(self.lstUser)
        layout.addWidget(self.lstInquiry)
        layout.addWidget(self.lstAdmin)
        layout.addWidget(self.tab, 10)
        self.setLayout(layout)

    def __info__(self):
        today = datetime.today()
        if self.author == '관리자':
            dataFrame = self.connInfo.dataFrameInfoAdmin()
            for row, lst in enumerate(dataFrame.values):
                start = datetime.strptime(lst[5], "%Y-%m-%d")
                end = datetime.strptime(lst[6], "%Y-%m-%d")
                if start <= today <= end:
                    DialogInfo(lst[2])
        dataFrame = self.connInfo.dataFrameInfoUser()
        for row, lst in enumerate(dataFrame.values):
            start = datetime.strptime(lst[5], "%Y-%m-%d")
            end = datetime.strptime(lst[6], "%Y-%m-%d")
            if start <= today <= end:
                DialogInfo(lst[2])

    def RefreshTimeUser(self):
        menu = self.itemUser[1]
        idx = self.currentTabs.index(menu)
        self.tab.removeTab(idx)
        self.tab.insertTab(idx, MainUserTime(self), menu)
        self.tab.setCurrentIndex(idx)

    def RefreshInquiryUser(self):
        menu = self.itemInquiry[0]
        idx = self.currentTabs.index(menu)
        self.tab.removeTab(idx)
        self.tab.insertTab(idx, MainInquiryUser(self), menu)
        self.tab.setCurrentIndex(idx)

    def RefreshTotalPerYear(self):
        menu = self.itemInquiry[1]
        idx = self.currentTabs.index(menu)
        self.tab.removeTab(idx)
        self.tab.insertTab(idx, MainTotalPerYear(self), menu)
        self.tab.setCurrentIndex(idx)

    def RefreshTotalPerUser(self):
        menu = self.itemInquiry[2]
        idx = self.currentTabs.index(menu)
        self.tab.removeTab(idx)
        self.tab.insertTab(idx, MainTotalPerUser(self), menu)
        self.tab.setCurrentIndex(idx)

    def RefreshNewUser(self):
        menu = self.itemAdmin[0]
        idx = self.currentTabs.index(menu)
        widget = MainNewUser(self)
        if len(widget.tblNewUser.dataFrame):
            self.tab.removeTab(idx)
            self.tab.insertTab(idx, MainNewUser(self), menu)
            self.tab.setCurrentIndex(self.currentTabs.index(menu))
        else:
            self.tab.removeTab(idx)
            self.currentTabs.remove(menu)
            DialogMassage('신청 대상이 없습니다.')

    def RefreshAdminUser(self):
        menu = self.itemAdmin[1]
        idx = self.currentTabs.index(menu)
        self.tab.removeTab(idx)
        self.tab.insertTab(idx, MainAdminUser(self), menu)
        self.tab.setCurrentIndex(idx)

    def RefreshAdminBusiness(self):
        menu = self.itemAdmin[2]
        idx = self.currentTabs.index(menu)
        self.tab.removeTab(idx)
        self.tab.insertTab(idx, MainAdminBusiness(self), menu)
        self.tab.setCurrentIndex(idx)

    def RefreshAdminDB(self):
        menu = self.itemAdmin[3]
        idx = self.currentTabs.index(menu)
        self.tab.removeTab(idx)
        self.tab.insertTab(idx, MainDatabase(self), menu)
        self.tab.setCurrentIndex(idx)

    def RefreshAdminInfo(self):
        menu = self.itemAdmin[4]
        idx = self.currentTabs.index(menu)
        self.tab.removeTab(idx)
        self.tab.insertTab(idx, MainAdminInfo(self), menu)
        self.tab.setCurrentIndex(idx)

    def __ObjectRefresh__(self):
        self.refreshUser = {
            self.itemUser[1]: self.RefreshTimeUser
        }
        self.refreshInquiry = {
            self.itemInquiry[0]: self.RefreshInquiryUser,
            self.itemInquiry[1]: self.RefreshTotalPerYear,
            self.itemInquiry[2]: self.RefreshTotalPerUser
        }
        self.refreshAdmin = {
            self.itemAdmin[0]: self.RefreshNewUser,
            self.itemAdmin[1]: self.RefreshAdminUser,
            self.itemAdmin[2]: self.RefreshAdminBusiness,
            self.itemAdmin[3]: self.RefreshAdminDB,
            self.itemAdmin[4]: self.RefreshAdminInfo
        }

    def keyPressEvent(self, QKeyEvent):
        if Qt.ControlModifier:
            if QKeyEvent.key() == Qt.Key_Q:
                dig = DialogMassage('프로그램을 종료하시겠습니까?\n저장하지 않은 정보가 있는지 확인 바랍니다.', question=True)
                if dig.value:
                    self.closeEvent = self.closePass
                    self.close()

    def closeQuestion(self, QCloseEvent):
        dig = DialogMassage('프로그램을 종료하시겠습니까?\n저장하지 않은 정보가 있는지 확인 바랍니다.', question=True)
        if dig.value:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def closePass(self, QCloseEvent):
        pass