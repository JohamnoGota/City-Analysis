import pandas as pd 
from datetime import date, timedelta

dfA = pd.read_csv("Morelia/No_accidentes_morelia_calles.csv")

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

years = getyear()

dfA['DayF'] = processDate(dfA['Day'])

result = dfA.groupby('DayF')['Accidents'].sum()


result.to_csv('Morelia_Accidentes_Diarios.csv')

# # Where we are now: we have to loop over the df to search all equal values for dates and add the numbers
# # Using itertuples allows us to access the rows as tuples 
# current_date = date('2024', '1', '1')
# for row in dfA.itertuples():
#     if current_date == row.DayF:
#         cur_sum += row.Accidents
#         temp = current_date
    

    
    

