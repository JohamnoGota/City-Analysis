import pandas as pd
from datetime import date

df = pd.read_csv("/Users/juanmagonzalez/VsCode/streamlit/first/Morelia/Accidentes_Morelia.csv")

df['Date_dt'] = df['Date_dt'].str.replace('-', ' ')

df['Date_dt'] = df['Date_dt'].str.split()

df['Date_dt'] = df['Date_dt'].apply(lambda lst: date(int(lst[0]), int(lst[1]), int(lst[2])))

print(type(df['Date_dt'][0]))