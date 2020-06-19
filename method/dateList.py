from datetime import datetime
from datetime import date
from pandas import Timedelta


def __returnDate__(year, month, day):
    weekend = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)']
    idx = date(year, month, day).weekday()
    return weekend[idx]


def __returnDayCount__(year, month):
    if month == 12:
        current_month = datetime(year, month, 1, 0, 0, 0)
        next_month = datetime(year + 1, 1, 1, 0, 0, 0)
        days = Timedelta(next_month - current_month).days
    else:
        current_month = datetime(year, month, 1, 0, 0, 0)
        next_month = datetime(year, month + 1, 1, 0, 0, 0)
        days = Timedelta(next_month - current_month).days
    return days


def returnDateList(year):
    year = int(year)
    dateList = []
    for month in range(1, 13):
        days = __returnDayCount__(year, month) + 1
        for day in range(1, days):
            textMonth = f"0{month}" if month < 10 else f"{month}"
            textDay = f"0{day}" if day < 10 else f"{day}"
            textDate = __returnDate__(year, month, day)
            dateList.append(f"{textMonth}/{textDay}{textDate}")
    return dateList
