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

y = getyear()

# l = []
# for i in range(10):
#     l.append(i)

for (idx, row) in enumerate(y.itertuples()):
    print(f"{idx}:{row}")

