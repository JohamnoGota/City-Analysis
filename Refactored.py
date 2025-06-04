import locale 
import pandas as pd
import streamlit as st
from datetime import date, timedelta
import tools

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

# Helper para convertir texto de periodo a días
def period(ans):
    ds = ans.split()
    if ds[1] == "días":
        return int(ds[0])
    if ds[1] == "meses":
        return int(ds[0]) * 30
    return 365

# =====================
# Interfaz de Streamlit
# =====================
st.title("Análisis de tráfico y relación con condiciones de lluvia")
st.header("Morelia")

# Selección de período
day_range = st.selectbox(
    "Selecciona el periodo de días",
    ("1 día", "7 días", "15 días", "30 días", "3 meses", "6 meses", "Todo el año"),
    index=1
)

date_range = st.slider(
    "Elige un rango de fechas",
    min_value = date(2024, 1, 1),
    max_value = date(2024, 12, 31),
    value = date(2024, 1, 1),
    format = "DD-MM-YY",
)

# Cálculo de fecha final
range = period(day_range)
start_time = date_range
end_time = start_time + timedelta(days=range)

st.write("Inicio:", start_time.strftime('%d %b %y'), "Fin:", end_time.strftime('%d %b %y'))

# ====================
# Carga y limpieza de datos
# ====================
# Carga y parseo directo de fechas
dfA = pd.read_csv("Morelia/Accidentes_Morelia.csv", parse_dates=["Date_dt"])
dfW = pd.read_csv("Morelia/Morelia_Lluvias.csv", parse_dates=["Date"])
dfT = pd.read_csv("Morelia/Morelia_Accidentes_Total.csv", parse_dates=["Date"])

# Limpieza con clase personalizada
trans = tools.dfTransform(dfT, format=True)
dfT = trans.convert_date().df  # Ahora solo convierte fechas
dfT = trans.addFilters().df

# Limpieza de dfA
dfA = dfA.iloc[::-1].drop(['Unnamed: 0'], axis=1)

# ====================
# Filtros por rango de fechas
# ====================
maskA = (dfA['Date_dt'] > start_time) & (dfA['Date_dt'] < end_time)
maskW = (dfW['Date'] > start_time) & (dfW['Date'] < end_time)
maskT = (dfT['Date'] > start_time) & (dfT['Date'] < end_time)

dfA_range = dfA[maskA]
dfW_range = dfW[maskW]
dfT_range = dfT[maskT]

# ====================
# Visualizaciones
# ====================
st.write("El número de accidentes para este periodo es:", dfT_range['Accidents'].sum())
st.write("La cantidad de Precipitación en este periodo es:", dfW_range['rain_sum'].sum())

st.map(dfA_range, size=2)
st.bar_chart(dfW_range, x='Date', y='rain_sum')
st.bar_chart(dfT_range, x='Date', y='Accidents')

# ====================
# Análisis adicional
# ====================
st.header("Exploración de datos")

st.bar_chart(dfT.groupby('WeekdayNum')['Accidents'].sum(), color='#ff7a73')
st.bar_chart(dfT.groupby('Month')['Accidents'].sum(), color='#aaeb8a')
st.bar_chart(dfT.groupby('WeekNum')['Accidents'].sum(), color='#f2d17e')
