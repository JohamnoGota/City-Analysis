import locale 
import pandas as pd
import streamlit as st
from datetime import datetime, date

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Español

def date_format(dateTemp):
    dateTemp = dateTemp.str.replace('-', ' ')

    dateTemp = dateTemp.str.split()

    dateTemp = dateTemp.apply(lambda lst: date(int(lst[0]), int(lst[1]), int(lst[2])))

    return dateTemp


date_range = st.slider(
    "Elige un rango de fechas",
    min_value = date(2024, 1, 1),
    max_value = date(2024, 12, 31),
    value= (date(2024, 1, 1), date(2024, 2, 1)) ,
    format="DD-MM-YY",
)

start_time = date_range[0]
end_time = date_range[1]

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