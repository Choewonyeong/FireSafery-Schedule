from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from material.ComboBox import CbxFilterInTable
from material.ComboBox import CbxToolInTable
from material.LineEdit import LdtAdminUserInTable
from material.LineEdit import LdtDateInTable
from material.PushButton import BtnPasswordInTable
from material.PushButton import BtnDeleteUserInTable
from setting.variables import itemUserPosition
from setting.variables import itemUserDegree
from setting.variables import itemUserStatus
from setting.variables import itemUserAuthor
from qss import Table


class TableAdminUser(QTableWidget):
    def __init__(self, widget):
        QTableWidget.__init__(self)
        self.setStyleSheet(Table.styleDefault)
        self.widget = widget
        self.__variables__()
        self.__setting__()
        self.__setFilter__()
        self.__setData__()

    def __variables__(self):
        self.editLog = []
        self.objects = []
        self.columns = self.widget.windows.connUser.dataFrameUser(column=True)+['비밀번호', '설정']
        self.dataFrame = self.widget.windows.connUser.dataFrameUser()
        del self.dataFrame[self.columns[14]]
        del self.dataFrame[self.columns[2]]
        self.columns.pop(14)
        self.columns.pop(2)

    def __setting__(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        self.verticalHeader().setVisible(False)

    def __setFilter__(self):
        self.insertRow(0)
        for idx, header in enumerate(self.columns):
            if header in ['비밀번호', '설정']:
                item = QTableWidgetItem('')
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(0, idx, item)
            elif header == '주민등록번호':
                items = self.dataFrame[header].drop_duplicates().tolist()
                i = 0
                p = []
                for item in items:
                    item = item.replace('-', '')
                    try:
                        items[i] = int(item)
                    except:
                        p.append(i)
                    i += 1
                p.reverse()
                for i in p:
                    items.pop(i)
                items.sort()
                for i, item in enumerate(items):
                    if len(str(item)) != 7:
                        items[i] = '0'*(7-len(str(item)))+str(item)
                items = ['전체'] + [f"{str(item)[:6]}-{str(item)[6]}" for item in items]
                CbxFilterInTable(idx, items, self)
            elif header == '연락처':
                items = self.dataFrame[header].drop_duplicates().tolist()
                i = 0
                p = []
                for item in items:
                    item = item.replace('-', '')
                    try:
                        items[i] = int(item)
                    except:
                        p.append(i)
                    i += 1
                p.reverse()
                for i in p:
                    items.pop(i)
                items.sort()
                items = ['전체'] + [f"0{str(item)[:2]}-{str(item)[2:6]}-{str(item)[6:]}" for item in items]
                CbxFilterInTable(idx, items, self)
            elif header == '과학기술인등록번호':
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
                item = QTableWidgetItem(data)
                item.setFlags(Qt.ItemIsEditable)
                self.setItem(row+1, col, item)
                if col in [1, 3, 4, 6, 7, 8, 9, 10]:
                    widget = LdtAdminUserInTable(row+1, col, data, self)
                    self.objects.append(widget)
                elif col == 2:
                    widget = CbxToolInTable(row+1, col, ['']+itemUserPosition, data, self)
                    self.objects.append(widget)
                elif col == 5:
                    widget = CbxToolInTable(row+1, col, ['']+itemUserDegree, data, self)
                    self.objects.append(widget)
                elif col == 11:
                    widget = CbxToolInTable(row+1, col, ['']+itemUserStatus, data, self)
                    self.objects.append(widget)
                elif col == 12:
                    widget = CbxToolInTable(row+1, col, ['']+itemUserAuthor, data, self)
                    self.objects.append(widget)
                elif col == 13:
                    LdtDateInTable(row+1, col, data, self)
            col = len(self.columns)-2
            BtnPasswordInTable('확인', self, row+1, col)
            col = col+1
            BtnDeleteUserInTable('삭제', self, row+1, col)
        self.resizeColumnsToContents()
        self.setColumnWidth(1, 80)
        self.setColumnWidth(3, 80)
        self.setColumnWidth(4, 120)
        self.setColumnWidth(5, 80)
        self.setColumnWidth(6, 140)
        self.setColumnWidth(7, 120)
        self.setColumnWidth(8, 80)
        self.setColumnWidth(9, 80)

    def UpdateEditDate(self, row, editDate):
        item = QTableWidgetItem(editDate)
        item.setFlags(Qt.ItemIsEditable)
        self.setItem(row, 13, item)

    def Show(self):
        for row in range(1, self.rowCount()):
            self.showRow(row)

    def Filter(self, col, filterText):
        self.Show()
        for row in range(1, self.rowCount()):
            if filterText == '전체':
                pass
            elif col in [2, 5, 11, 12] and self.cellWidget(row, col).currentText() != filterText:
                self.hideRow(row)
            elif col not in [2, 5, 11, 12] and self.cellWidget(row, col).text() != filterText:
                self.hideRow(row)
