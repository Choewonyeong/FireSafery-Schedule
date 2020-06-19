from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from connector.connDB import connDB
from material.ComboBox import CbxNewBusiness
from material.Label import LblNewBusiness
from material.LineEdit import LdtNewBusiness
from material.PushButton import BtnSubmit
from material.PushButton import BtnCancel
from component.dialog.DialogMassage import DialogMassage
from qss.Dialog import styleGeneral
from datetime import datetime


class DialogNewBusiness(QDialog):
    def __init__(self, widget):
        QDialog.__init__(self)
        self.setStyleSheet(styleGeneral)
        self.widget = widget
        self.__setting__()
        self.__connector__()
        self.__variables__()
        self.__component__()
        self.exec_()

    def __setting__(self):
        self.setWindowFlag(Qt.FramelessWindowHint)

    def __connector__(self):
        self.connDB = connDB(self.widget.windows.CURRENT_YEAR)

    def __variables__(self):
        pass

    def __component__(self):
        self.__label__()
        self.__inputWidgets__()
        self.__pushButton__()
        self.__layout__()

    def __label__(self):
        lblTitle = LblNewBusiness('사업명')
        lblCode = LblNewBusiness('사업코드')
        lblForm = LblNewBusiness('사업형태')
        lblOrder = LblNewBusiness('발주처')
        lblSummary = LblNewBusiness('사업요약')
        lblStart = LblNewBusiness('시작일')
        lblEnd = LblNewBusiness('종료일')
        lblMonth = LblNewBusiness('개월수')
        lblMax = LblNewBusiness('보존기간')
        lblMaster = LblNewBusiness('사업책임자')
        lblPL = LblNewBusiness('PL')
        lblAdmin = LblNewBusiness('기술행정')
        lblPrice = LblNewBusiness('사업비')
        lblStatus = LblNewBusiness('진행상태')
        self.objectLabel = [lblTitle,
                            lblCode,
                            lblForm,
                            lblOrder,
                            lblSummary,
                            lblStart,
                            lblEnd,
                            lblMonth,
                            lblMax,
                            lblMaster,
                            lblPL,
                            lblAdmin,
                            lblPrice,
                            lblStatus]
        for lbl in self.objectLabel:
            lbl.setFixedWidth(80)

    def __inputWidgets__(self):
        ldtTitle = LdtNewBusiness(essential=True)
        ldtCode = LdtNewBusiness(essential=True)
        cbxForm = CbxNewBusiness(['기술', '연구', '국책', '일반', '기타'], '기술')
        ldtOrder = LdtNewBusiness()
        tedSummary = LdtNewBusiness()
        ldtStart = LdtNewBusiness(holderText='ex) 2014-02-28')

        def ldtStartEdit(text):
            start = text
            end = ldtEnd.text()
            try:
                start = datetime.strptime(start, '%Y-%m-%d')
                end = datetime.strptime(end, '%Y-%m-%d')
                yearCnt = (end.year - start.year)*12
                monthCnt = end.month - start.month
                totalCnt = yearCnt + monthCnt
                self.objectInput[7].setText(str(totalCnt))
            except:
                pass
        ldtStart.textEdited.connect(ldtStartEdit)

        def ldtEndEdit(text):
            start = ldtStart.text()
            end = text
            try:
                start = datetime.strptime(start, '%Y-%m-%d')
                end = datetime.strptime(end, '%Y-%m-%d')
                yearCnt = (end.year - start.year)*12
                monthCnt = end.month - start.month
                totalCnt = yearCnt + monthCnt
                self.objectInput[7].setText(str(totalCnt))
            except:
                pass
        ldtEnd = LdtNewBusiness(holderText='ex) 2019-06-10')
        ldtEnd.textEdited.connect(ldtEndEdit)
        ldtMonth = LdtNewBusiness(enabled=False)
        ldtMax = LdtNewBusiness(holderText='ex) 2020-06-10')
        ldtMaster = LdtNewBusiness(holderText='ex) 김재환')
        ldtPL = LdtNewBusiness(holderText='ex) 김재환')
        ldtAdmin = LdtNewBusiness(holderText='ex) 진수경')

        def ldtPriceEdit(text):
            sender = self.sender()
            try:
                price = int(text.replace(',', ''))
                price = format(price, ',')
                sender.setText(price)
            except:
                pass
        ldtPrice = LdtNewBusiness()
        ldtPrice.textEdited.connect(ldtPriceEdit)
        cbxStatus = CbxNewBusiness(['수주', '진행', '중단', '준공', 'A/S'], '진행')
        self.objectInput = [ldtTitle,
                            ldtCode,
                            cbxForm,
                            ldtOrder,
                            tedSummary,
                            ldtStart,
                            ldtEnd,
                            ldtMonth,
                            ldtMax,
                            ldtMaster,
                            ldtPL,
                            ldtAdmin,
                            ldtPrice,
                            cbxStatus]

    def __pushButton__(self):
        def btnCloseClick():
            self.close()
        self.btnClose = BtnCancel('닫기', btnCloseClick)

        def btnInsertClick():
            businessInfo = []
            for idx, info in enumerate(self.objectInput):
                if idx in [2, 13]:
                    businessInfo.append(info.currentText())
                else:
                    businessInfo.append(info.text())
            if businessInfo[0] == '':
                DialogMassage('사업명을 입력하세요.')
            elif businessInfo[1] == '':
                DialogMassage('사업코드를 입력하세요.')
            else:
                number = self.widget.windows.connBusiness.insertBusiness(businessInfo)
                self.connDB.insertNewBusiness(number)
                self.widget.windows.RefreshAdminBusiness()
                DialogMassage('새로운 사업 정보가 등록되었습니다.')
                self.close()

        self.btnInsert = BtnSubmit('등록', btnInsertClick, default=True)

    def __layout__(self):
        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnClose)
        layoutBtn.addWidget(self.btnInsert)
        layout = QVBoxLayout()
        for lbl, widget in zip(self.objectLabel, self.objectInput):
            layoutObjects = QHBoxLayout()
            layoutObjects.addWidget(lbl)
            layoutObjects.addWidget(widget)
            layout.addLayout(layoutObjects)
        layout.addLayout(layoutBtn)
        self.setLayout(layout)
