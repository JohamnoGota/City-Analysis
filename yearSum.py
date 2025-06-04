import pandas as pd 
from datetime import date, timedelta

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

dates = getyear()
idx = 0
for row in dates.itertuples():
    dates.at[idx, row.TotalAccidents] = dates.at[idx, row.TotalAccidents] + 1