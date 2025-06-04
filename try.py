import pandas as pd

df = pd.read_csv("/Users/juanmagonzalez/VsCode/streamlit/first/Accidentes.csv")

coordinates = df.loc[:,["Latitude", "Longitude"]]