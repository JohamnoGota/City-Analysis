from datetime import date, timedelta
import pandas as pd


def getyear():
    od = date(2024, 1, 1)

    dates = []
    for i in range(366):
        current =  od + timedelta(days=i)
        dates.append(current)

    year = pd.DataFrame()

    year['Date'] = pd.Series(dates)
    year['TotalAccidents'] = 0

    return year

print(getyear())