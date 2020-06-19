from sqlite3 import connect
from datetime import datetime
from pandas import DataFrame
from component.dialog.DialogMassage import DialogMassage
import setting


class connInfo:
    def __init__(self):
        self.path = setting.databaseInfo

    def __conn__(self):
        conn = connect(self.path, isolation_level=None)
        return conn

    def dataFrameInfo(self, column=False):
        try:
            conn = self.__conn__()
            query = "select * from Info;"
            run = conn.execute(query)
            columns = [column[0] for column in run.description]
            if column:
                conn.close()
                return columns
            data = conn.execute(query).fetchall()
            dataFrame = DataFrame(data=data, columns=columns)
            conn.close()
            return dataFrame
        except Exception as e:
            DialogMassage(f'../connInfo.py/dataFrameInfo : {e}')
            return [[]]

    def dataFrameInfoUser(self):
        try:
            conn = self.__conn__()
            query = "select * from Info Where not `대상`='관리자' and `사용여부`='사용';"
            run = conn.execute(query)
            columns = [column[0] for column in run.description]
            data = conn.execute(query).fetchall()
            dataFrame = DataFrame(data=data, columns=columns)
            conn.close()
            return dataFrame
        except Exception as e:
            DialogMassage(f'../connInfo.py/dataFrameInfoUser : {e}')
            return [[]]

    def dataFrameInfoAdmin(self):
        try:
            conn = self.__conn__()
            query = "select * from Info Where `대상`='관리자' and `사용여부`='사용';"
            run = conn.execute(query)
            columns = [column[0] for column in run.description]
            data = conn.execute(query).fetchall()
            dataFrame = DataFrame(data=data, columns=columns)
            conn.close()
            return dataFrame
        except Exception as e:
            DialogMassage(f'../connInfo.py/dataFrameInfo : {e}')
            return [[]]

    def insertInfo(self, infoInfo):
        """
        infoInfo = [number, option, text, used, target, startDate, endDate]
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = self.__conn__()
            query = f"insert into Info Values(?, ?, ?, ?, ?, ?, ?, ?);"
            conn.execute(query, infoInfo+[now])
            conn.close()
        except Exception as e:
            DialogMassage(f'../connInfo.py/insertInfo : {e}')

    def updateInfo(self, header, data, number):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = self.__conn__()
            query = f"update Info set `{header}`='{data}', `수정한날짜`='{now}' Where `번호`='{number}';"
            conn.execute(query)
            conn.close()
            return now
        except Exception as e:
            DialogMassage(f'../connInfo.py/updateInfo : {e}')
            return now

    def deleteInfo(self, number):
        try:
            conn = self.__conn__()
            query = f"delete from Info Where `번호`='{number}';"
            conn.execute(query)
            conn.close()
        except Exception as e:
            DialogMassage(f'../connInfo.py/deleteInfo : {e}')

    def returnNumber(self):
        try:
            conn = self.__conn__()
            query = "select `번호` from Info;"
            run = conn.execute(query)
            numbers = [number[0] for number in run.fetchall()]
            number = numbers.pop()
            number = str(int(number) + 1)
            return number
        except Exception as e:
            DialogMassage(f'../connInfo.py/returnNumber : {e}')
            return '1'
