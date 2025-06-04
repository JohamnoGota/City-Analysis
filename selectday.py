import locale 
import pandas as pd
import streamlit as st
from datetime import date, timedelta

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Español

def period(ans):
    ds = ans.split()

    if ds[1] == "días":
        return int(ds[0])
    if ds[1] == "meses":
        return int(ds[0]) * 30
    return 365

     

def date_format(dateTemp):
    dateTemp = dateTemp.str.replace('-', ' ')
    dateTemp = dateTemp.str.split()
    dateTemp = dateTemp.apply(lambda lst: date(int(lst[0]), int(lst[1]), int(lst[2])))
    return dateTemp
  
day_range = st.selectbox(
    "Selecciona el periodo de días",
    ("1 día", "7 días", "15 días", "30 días", "3 meses", "6 meses", "Todo el año"),
    index= 1,
    placeholder="Selecciona un periodo..."
)   


date_range = st.slider(
    "Elige un rango de fechas",
    min_value = date(2024, 1, 1),
    max_value = date(2024, 12, 31),
    value= date(2024, 1, 1),
    format="DD-MM-YY",
)


range = period(day_range)
st.write(day_range, range)
start_time = date_range
end_time = date_range + timedelta(days=range)

# st.write("Inicio:", start_time)

start_format = start_time.strftime('%d') + " " +  start_time.strftime('%b') + " " + start_time.strftime('%y')
end_format = end_time.strftime('%d') + " " +  end_time.strftime('%b') + " " + end_time.strftime('%y')

st.write("Inicio:", start_format, "Fin:", end_format)



dfA = pd.read_csv("/Users/juanmagonzalez/VsCode/streamlit/WeatherMap/Morelia/Accidentes_Morelia.csv")
dfW = pd.read_csv("Morelia/LluviaMorelia2024.csv")
# dfA['Date'] = pd.to_datetime(dfA['Date'], infer_datetime_format=True)
# dfA = dfA.sort_values(by=['Date'] )


dfA = dfA.iloc[::-1]
dfA = dfA.drop(['Unnamed: 0'], axis=1)

dfA['Date_dt'] = date_format(dfA['Date_dt'])

dfW['Date'] = date_format(dfW['Date'])

maskA = (dfA['Date_dt'] > start_time) & (dfA['Date_dt'] < end_time)
maskW = (dfW['Date'] > start_time) & (dfW['Date'] < end_time)

dfA_range = dfA[maskA]
dfW_range = dfW[maskW]
# dfA_range = dfA 
st.map(dfA_range, size=2)
st.bar_chart(dfW_range, x='Date', y='rain_sum')