from sqlite3 import connect
from pandas import DataFrame
from component.dialog.DialogMassage import DialogMassage
import setting


def returnBusinesses(year):
    try:
        conn = connect(f"{setting.databaseMain}/{year}.db")
        query = f"select `사업명` From Main Where `적용상태_사업`='적용' and `적용상태_부서원`='적용' order by `번호`;"
        run = conn.execute(query)
        dataFrame = DataFrame(data=run.fetchall(), columns=['사업명'])
        conn.close()
        businesses = dataFrame['사업명'].drop_duplicates().tolist()
        return businesses
    except Exception as e:
        DialogMassage(f'../connTotal.py/returnBusinesses : {e}')


def returnColumns(year):
    try:
        conn = connect(f"{setting.databaseMain}/{year}.db")
        query = f"select * From Main;"
        run = conn.execute(query)
        columns = [data[0] for data in run.description]
        conn.close()
        return columns
    except Exception as e:
        DialogMassage(f'../connTotal.py/returnColumns : {e}')
        return []


def runQuery_return(year, query):
    try:
        conn = connect(f"{setting.databaseMain}/{year}.db")
        run = conn.execute(query)
        total = [0.0 if not value else float(value) for value in run.fetchall()[0]]
        conn.close()
        return total
    except Exception as e:
        DialogMassage(f'../connTotal.py/runQuery_return : {e}')
        return [0]
