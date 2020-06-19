from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from connector.connBusiness import connBusiness
from material.ComboBox import CbxToolInTable
from material.ComboBox import CbxFilterInTable
from material.LineEdit import LdtAdminBusinessInTable
from material.LineEdit import LdtDateInTable
from material.PushButton import BtnDeleteBusinessInTable
from datetime import datetime


class TableAdminBusiness(QTableWidget):
    def __init__(self, widget):
        QTableWidget.__init__(self)
        self.widget = widget
        self.__connector__()
        self.__variables__()
        self.__setting__()
        self.__setFilter__()
        self.__setData__()

    def __connector__(self):
        self.connBusiness = connBusiness()

    def __variables__(self):
        self.editLog = []
        self.objects = []
        self.columns = self.widget.windows.connBusiness.dataFrameBusiness(column=True)+['설정']
        self.dataFrame = self.widget.windows.connBusiness.dataFrameBusiness()
        self.dataFrame = self.dataFrame.drop([0, len(self.dataFrame)-1])

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)

    def __setFilter__(self):
        self.insertRow(0)
        for idx, header in enumerate(self.columns):
            if header in ['번호', '설정']:
                item = QTableWidgetItem('')
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(0, idx, item)
            elif header == '개월수':
                items = self.dataFrame[header].drop_duplicates().tolist()
                i = 0
                p = []
                for item in items:
                    try:
                        items[i] = int(item)
                    except:
                        p.append(i)
                    i += 1
                p.reverse()
                for i in p:
                    items.pop(i)
                items.sort()
                items = ['전체'] + [str(item) for item in items]
                CbxFilterInTable(idx, items, self)
            elif header == '사업비':
                items = self.dataFrame[header].drop_duplicates().tolist()
                i = 0
                p = []
                for item in items:
                    item = item.replace(',', '')
                    try:
                        items[i] = int(item)
                    except:
                        p.append(i)
                    i += 1
                p.reverse()
                for i in p:
                    items.pop(i)
                items.sort()
                items = ['전체'] + [format(item, ',') for item in items]
                CbxFilterInTable(idx, items, self)
            else:
                items = self.dataFrame[header].drop_duplicates().tolist()
                if '' in items:
                    items.remove('')
                items.sort()
                items = ['전체'] + items
                CbxFilterInTable(idx, items, self)

    def __setData__(self):
        for row, lst in enumerate(self.dataFrame.values):
            self.insertRow(row+1)
            self.setRowHeight(row+1, 40)
            for col, data in enumerate(lst):
                data = str(data)
                item = QTableWidgetItem(data)
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(row+1, col, item)
                if col in [1, 2, 4, 10, 11, 12]:
                    widget = LdtAdminBusinessInTable(row+1, col, data, self)
                    self.objects.append(widget)
                elif col == 3:
                    widget = CbxToolInTable(row+1, col, ['기술', '연구', '국책', '일반', '기타'], data, self)
                    self.objects.append(widget)
                elif col == 5:
                    widget = LdtAdminBusinessInTable(row+1, col, data, self)
                    widget.setAlignment(Qt.AlignLeft)
                    self.objects.append(widget)
                elif col in [6, 7]:
                    widget = LdtAdminBusinessInTable(row+1, col, data, self)
                    widget.textEdited.connect(self.TableLineEditChange)
                    self.objects.append(widget)
                elif col == 8:
                    widget = LdtAdminBusinessInTable(row+1, col, data, self)
                    widget.setEnabled(False)
                    self.objects.append(widget)
                elif col == 9:
                    widget = LdtAdminBusinessInTable(row+1, col, data, self)
                    self.objects.append(widget)
                elif col == 13:
                    data = data.replace(' ', '')
                    widget = LdtAdminBusinessInTable(row+1, col, data, self)
                    widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.objects.append(widget)
                elif col == 14:
                    widget = CbxToolInTable(row+1, col, ['수주', '진행', '중단', '준공', 'A/S'], data, self)
                    self.objects.append(widget)
                elif col == 15:
                    LdtDateInTable(row+1, col, data, self)

            col = len(self.columns)-1
            BtnDeleteBusinessInTable('삭제', self, row+1, col)
        self.resizeColumnsToContents()
        self.hideColumn(0)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(8, 50)
        for col in [6, 7, 9]:
            self.setColumnWidth(col, 100)
        for col in [10, 11, 12]:
            self.setColumnWidth(col, 80)

    def UpdateEditDate(self, row, editDate):
        item = QTableWidgetItem(editDate)
        item.setFlags(Qt.ItemIsEditable)
        self.setItem(row, 15, item)

    def TableLineEditChange(self):
        row = self.sender().row
        widgetStart = self.cellWidget(row, 6)
        widgetEnd = self.cellWidget(row, 7)
        widgetTotal = self.cellWidget(row, 8)
        start = widgetStart.text()
        end = widgetEnd.text()
        try:
            start = datetime.strptime(start, "%Y-%m-%d")
            end = datetime.strptime(end, "%Y-%m-%d")
            yearCnt = (end.year - start.year)*12
            monthCnt = end.month - start.month
            totalCnt = yearCnt + monthCnt
            widgetTotal.setText(str(totalCnt))
        except:
            pass

    def Show(self):
        for row in range(1, self.rowCount()-1):
            self.showRow(row)

    def Filter(self, col, filterText):
        self.Show()
        for row in range(1, self.rowCount()):
            if filterText == '전체':
                pass
            elif col in [3, 14] and self.cellWidget(row, col).currentText() != filterText:
                self.hideRow(row)
            elif col not in [3, 14] and self.cellWidget(row, col).text() != filterText:
                self.hideRow(row)