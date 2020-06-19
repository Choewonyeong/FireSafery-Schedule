from sqlite3 import connect
from pandas import DataFrame
from method.dateList import returnDateList
from component.dialog.DialogMassage import DialogMassage
from connector.connUser import connUser
from connector.connBusiness import connBusiness
import setting


class connDB:
    def __init__(self, year):
        self.year = year
        self.path = f"{setting.databaseMain}/{year}.db"
        self.connUser = connUser()
        self.connBusiness = connBusiness()

    def __conn__(self):
        conn = connect(self.path, isolation_level=None)
        return conn

    def createDB(self):
        step_1 = self.__createDatabase__()
        step_2 = self.__createSource__()
        step_3 = self.__insertSource__()
        step_4 = self.__alterDateColumns__()
        if step_1 and step_2 and step_3 and step_4:
            DialogMassage('데이터베이스 생성이 완료되었습니다.')
        else:
            DialogMassage('데이터베이스가 이미 존재합니다.')

    def __createDatabase__(self):
        try:
            conn = self.__conn__()
            query = """
            Create Table Main(
                `번호` Integer,
                `사업명` Text default '',
                `사업코드` Text default '',
                `구분` Text default '',
                `적용상태_사업` Text default '',
                `계정` Text default '',
                `성명` Text default '',
                `적용상태_부서원` Text default '');"""
            conn.execute(query)
            conn.close()
            return True
        except Exception as e:
            DialogMassage(f'../connDB.py/__createDatabase__ : {e}')
            return False

    def __createSource__(self):
        try:
            self.sourceUser = self.connUser.returnSources()
            sourceBusiness = self.connBusiness.returnSources()
            self.sourceBusiness = []
            for idx, source in enumerate(sourceBusiness):
                if source[0] == 0:
                    for option in ['회의', '교육/훈련', '기타업무']:
                        self.sourceBusiness.append(source+[option])
                if source[0] != 0:
                    for option in ['사업관리', '기술업무']:
                        self.sourceBusiness.append(source+[option])
            return True
        except Exception as e:
            DialogMassage(f'../connDB.py/__createSource__ : {e}')
            return False

    def __insertSource__(self):
        try:
            conn = self.__conn__()
            for userSource in self.sourceUser:
                for idx, businessSource in enumerate(self.sourceBusiness):
                    query = f"insert into Main Values(?, ?, ?, ?, ?, ?, ?, ?);"
                    conn.execute(query, businessSource+['적용']+userSource+['적용'])
            conn.close()
            return True
        except Exception as e:
            DialogMassage(f'../connDB.py/__insertSource__ : {e}')
            return False

    def __alterDateColumns__(self):
        dateList = returnDateList(self.year)
        try:
            conn = self.__conn__()
            for textDate in dateList:
                query = f"alter table Main add column `{textDate}` Text default '';"
                conn.execute(query)
            conn.close()
            return True
        except Exception as e:
            DialogMassage(f'../connDB.py/__alterDateColumns__ : {e}')
            return False

    def dataFrameUser(self, column=False):
        try:
            conn = self.__conn__()
            query = "select `계정`, `성명`, `적용상태_부서원` from Main;"
            run = conn.execute(query)
            columns = [column[0] for column in run.description]
            if column:
                conn.close()
                return columns
            data = conn.execute(query).fetchall()
            dataFrame = DataFrame(data=data, columns=columns)
            dataFrame = dataFrame.drop_duplicates(columns[0])
            conn.close()
            return dataFrame
        except Exception as e:
            DialogMassage(f'../connDB.py/dataFrameUser : {e}')
            return [[]]

    def dataFrameBusiness(self, column=False):
        try:
            conn = self.__conn__()
            query = "select `번호`, `사업명`, `사업코드`, `적용상태_사업` from Main Order by `번호`;"
            run = conn.execute(query)
            columns = [column[0] for column in run.description]
            if column:
                conn.close()
                return columns
            data = conn.execute(query).fetchall()
            dataFrame = DataFrame(data=data, columns=columns)
            dataFrame = dataFrame.drop_duplicates(columns[0])
            conn.close()
            return dataFrame
        except Exception as e:
            DialogMassage(f'../connDB.py/dataFrameBusiness : {e}')
            return [[]]

    def dataFramePerUserTime(self, account, column=False):
        try:
            conn = self.__conn__()
            query = f"select * from Main where `계정`='{account}' and `적용상태_사업`='적용' and `적용상태_부서원`='적용' Order by `번호`;"
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
            DialogMassage(f'../connDB.py/dataFramePerUserTime : {e}')
            return [[]]

    def dataFramePerUserBusiness(self, account, column=False):
        try:
            conn = self.__conn__()
            query = f"select `번호`, `사업명`, `사업코드`, `구분` from Main where `계정`='{account}' and `적용상태_사업`='적용' and `적용상태_부서원`='적용' Order by `번호`;"
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
            DialogMassage(f'../connDB.py/dataFramePerUserBusiness : {e}')
            return [[]]

    def updateUserApplyStatus(self, value, account):
        """
        value = ['적용', '제외']
        """
        try:
            conn = self.__conn__()
            query = f"update Main set `적용상태_부서원`='{value}' Where `계정`='{account}';"
            conn.execute(query)
            conn.close()
        except Exception as e:
            DialogMassage(f'../connDB.py/updateUserApplyStatus : {e}')

    def updateBusinessApplyStatus(self, value, number):
        """
        value = ['적용', '제외']
        """
        try:
            conn = self.__conn__()
            query = f"update Main set `적용상태_사업`='{value}' Where `번호`='{number}';"
            conn.execute(query)
            conn.close()
        except Exception as e:
            DialogMassage(f'../connDB.py/updateBusinessApplyStatus : {e}')

    def listTotal(self, columns, account):
        try:
            conn = self.__conn__()
            sumQuery = f"SUM(`{'`), SUM(`'.join(columns)}`)"
            query = f"select {sumQuery} from Main Where `계정`='{account}' and `적용상태_사업`='적용' and `적용상태_부서원`='적용';"
            run = conn.execute(query)
            total = [float(value) for value in run.fetchall()[0]]
            conn.close()
            return total
        except Exception as e:
            DialogMassage(f'../connDB.py/listTotal : {e}')
            return []

    def updateUserTime(self, column, value, number, option, account):
        try:
            conn = self.__conn__()
            query = f"update Main set `{column}`='{value}' Where `번호`='{number}' and `구분`='{option}' and `계정`='{account}';"
            conn.execute(query)
            conn.close()
        except Exception as e:
            DialogMassage(f'../connDB.py/updateUserTime : {e}')

    def insertNewBusiness(self, number):
        try:
            conn = self.__conn__()
            businessInfo = self.connBusiness.returnSource(number)
            sourceBusiness = []
            if businessInfo[0] == '0':
                for option in ['회의', '교육/훈련', '기타업무']:
                    sourceBusiness.append(businessInfo+[option])

            if businessInfo[0] != '0':
                for option in ['사업관리', '기술업무']:
                    sourceBusiness.append(businessInfo+[option])

            for userSource in self.connUser.returnSources():
                for idx, businessSource in enumerate(sourceBusiness):
                    query = f"""insert into Main(`번호`, `사업명`, `사업코드`, `구분`, `적용상태_사업`, 
                                `계정`, `성명`, `적용상태_부서원`) Values(?, ?, ?, ?, ?, ?, ?, ?);"""
                    conn.execute(query, businessSource+['적용']+userSource+['적용'])
            conn.close()
        except Exception as e:
            DialogMassage(f'../connDB.py/insertNewBusiness : {e}')

    def insertNewUser(self, account):
        try:
            conn = self.__conn__()
            userInfo = self.connUser.returnSource(account)
            businessInfo = self.connBusiness.returnSources()
            sourceBusiness = []
            for idx, source in enumerate(businessInfo):
                if source[0] == '0':
                    for option in ['회의', '교육/훈련', '기타업무']:
                        sourceBusiness.append(source+[option])
                if source[0] != '0':
                    for option in ['사업관리', '기술업무']:
                        sourceBusiness.append(source+[option])

            for idx, businessSource in enumerate(sourceBusiness):
                query = f"""insert into Main(`번호`, `사업명`, `사업코드`, `구분`, `적용상태_사업`, 
                            `계정`, `성명`, `적용상태_부서원`) Values(?, ?, ?, ?, ?, ?, ?, ?);"""
                conn.execute(query, businessSource+['적용']+userInfo+['적용'])
            conn.close()
        except Exception as e:
            DialogMassage(f'../connDB.py/insertNewUser : {e}')

    def deleteBusiness(self, number):
        try:
            conn = self.__conn__()
            query = f"delete from Main where `번호`='{number}';"
            conn.execute(query)
            conn.close()
        except Exception as e:
            DialogMassage(f'../connDB.py/deleteBusiness : {e}')

    def deleteUser(self, account):
        try:
            conn = self.__conn__()
            query = f"delete from Main where `계정`='{account}';"
            conn.execute(query)
            conn.close()
        except Exception as e:
            DialogMassage(f'../connDB.py/deleteUser : {e}')
