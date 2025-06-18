import locale 
import pandas as pd
import streamlit as st
from datetime import date, timedelta
from tools import DataFrameCleanUp

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


st.title("Análisis de tráfico y relación con condiciones de lluvia")
st.header("Morelia")



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


# Definición de los dataframes principales
dfA = pd.read_csv("Morelia/Accidentes_Morelia.csv")
dfW = pd.read_csv("Morelia/Morelia_Lluvias.csv")
dfT = pd.read_csv("Morelia/Morelia_Accidentes_Total.csv")

# Utilización de la clase DataFrameCleanUp para el manejo de las fechas de los dataframes

trans = (
    DataFrameCleanUp(dfT, date_column='Date', format=True)
    .convert_location()
    .convert_date()
    .addFilters()

)



# trans = tools.dfTransform(dfT, format=True)
# trans.convert(format=True)
dfT = trans.df
dfA = dfA.iloc[::-1]
dfA = dfA.drop(['Unnamed: 0'], axis=1)

dfA['Date_dt'] = date_format(dfA['Date_dt'])

dfW['Date'] = date_format(dfW['Date'])

maskA = (dfA['Date_dt'] > start_time) & (dfA['Date_dt'] < end_time)
maskW = (dfW['Date'] > start_time) & (dfW['Date'] < end_time)
maskSum = (dfT['Date_tuple'] > start_time) & (dfT['Date_tuple'] < end_time)

num_accidents = dfT[maskSum]['Accidents'].sum()
num_rain = dfW[maskW]['rain_sum'].sum()

st.write("El número de accidentes para este periodo es:", num_accidents)
st.write("La cantidad de Precipitación en este periodo es:", num_rain)
dfA_range = dfA[maskA]
dfW_range = dfW[maskW]
dfT_range = dfT[maskSum]

# dfA_range = dfA 
st.map(dfA_range, size=2)
st.bar_chart(dfW_range, x='Date', y='rain_sum', stack=False)
st.bar_chart(dfT_range, x='Date', y='Accidents', stack=False)

st.header("Exploración de datos")

st.write("Existen patrones para normalizar que deben tomarse en cuenta para un análisis más profundo." \
"La correlación principal para accidentes de tráfico es la cantidad de tráfico que existe en primer lugar. Mientras más concurrida está la ciudad más accidentes suceden " \
"Es por esto que la mayoria de accidentes ocurren en la semana de trabajo")

# dfT = trans.addFilters()
temp  = dfT.groupby('WeekdayNum')['Accidents'].sum()

st.bar_chart(temp, color='#ff7a73', stack=False)


temp  = dfT.groupby('Month')['Accidents'].sum()
st.bar_chart(temp, color='#aaeb8a', stack=False)

temp  = dfT.groupby('WeekNum')['Accidents'].sum()
st.bar_chart(temp, color='#f2d17e', stack=False)

# dfT.groupby('Month')['Total Accidents']
# dfT.groupby('WeekNum')['Total Accidents']

# ADDING TRAFFIC IRREGULARITIES 

st.header("Irregularidades de Tráfico, una clase posible")

st.write("Un análisis subsecuente de las condiciones de tráfico en días de lluvia pueden darnos más razones de la percepción de que la lluvia lleva a más accidentes")

dfI = pd.read_csv("Morelia/Morelia_Irregularidades_Causa.csv")
irr = (
    DataFrameCleanUp(dfI, date_column='Day', format=False)
    .convert_date()
    .addFilters()
    )


dfI = irr.df
print(dfI.dtypes)
dfI_counts = dfI['Date_tuple'].value_counts().reset_index()
print(type(dfI_counts))
dfI_counts.columns = ['Date_tuple', 'Count']
dfI_counts = dfI_counts.sort_values('DatePython')

print(dfI_counts)
# st.bar_chart(dfI_counts, color='#f2d17e', stack=False)
