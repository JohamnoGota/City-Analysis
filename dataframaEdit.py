import pandas as pd
import re

df = pd.read_csv("Morelia/waze_accidentes_morelia.csv")

# print(df.to_string())

points = (df['Location'])

lats = []
longs = []
for item in points.items():
    s = item[1]
    coord = re.findall(r"[0-9]+\.[0-9]+", s)
    longs.append(float(coord[0]) * - 1)

    lats.append(float(coord[1]))
    # lat = re.findall("-[0-9]+\.[0-9]+", s)

# print(lats)
# print(longs)

s_lat = pd.Series(lats)
s_long = pd.Series(longs)

df = df.drop(['Location', 'Avg Reliability'], axis=1)

df.insert(4, "LONGITUDE", s_long)
df.insert(4, "LATITUDE", s_lat)

# long va en el 4 y lat en el 5 

# Sección para cambiar el formato de fecha 

month_map = {
    'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
    'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
    'sept': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
}

def replace_months(date_str):
    for esp, eng in month_map.items():
        if esp in date_str:
            return date_str.replace(esp, eng)
    return date_str

# Apply the replacement and convert to datetime
df['Date_dt'] = df['Date'].apply(replace_months)
df['Date_dt'] = pd.to_datetime(df['Date_dt'], format='%d %b %Y')

# Convert to numeric (e.g., timestamp)
df['Date_numeric'] = df['Date_dt'].apply(lambda x: x.timestamp())





df.to_csv('Accidentes_Morelia.csv')