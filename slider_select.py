import locale 
import pandas as pd
import streamlit as st
from datetime import datetime, date

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Español

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



df = pd.read_csv("Morelia/Accidentes_Morelia.csv")

# df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
# df = df.sort_values(by=['Date'] )


df = df.iloc[::-1]
df = df.drop(['Unnamed: 0'], axis=1)

df['Date_dt'] = df['Date_dt'].str.replace('-', ' ')

df['Date_dt'] = df['Date_dt'].str.split()

df['Date_dt'] = df['Date_dt'].apply(lambda lst: date(int(lst[0]), int(lst[1]), int(lst[2])))



mask = (df['Date_dt'] > start_time) & (df['Date_dt'] < end_time)

df_range = df[mask]
# df_range = df 
st.map(df_range, size=2)