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


def replace_months(date_str):
    month_map = {
    'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
    'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
    'sept': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
    }

    for esp, eng in month_map.items():
        if esp in date_str:
            return date_str.replace(esp, eng)
    return date_str

def processDate(date_series):

    # Apply the replacement and convert to datetime
    date_series = date_series.apply(replace_months)
    date_format = pd.to_datetime(date_series, format='%d %b %Y')

    # # Convert to numeric (e.g., timestamp)
    # df['Date_numeric'] =date_format.apply(lambda x: x.timestamp())

    return date_format 
