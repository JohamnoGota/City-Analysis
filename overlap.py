import pandas as pd 
import matplotlib.pyplot as plt

dfA = pd.read_csv("/Users/juanmagonzalez/VsCode/streamlit/WeatherMap/Morelia/Accidentes_Morelia.csv")
dfA = dfA.iloc[::-1]
dfA = dfA.drop(['Unnamed: 0'], axis=1)

dfA['Date_dt'] = date_format(dfA['Date_dt'])

plt.bar(dfA['Category'], dfA['Values'], color='skyblue')
plt.xlabel("Date")
plt.ylabel("Values")
plt.title("Bar Chart Example")
plt.show()