import pandas as pd
from datetime import date
import re 


"""
    Clase de base para la limpieza y extracción eficiente de los datos de archivso waze CSV

"""
class DataFrameCleanUp:
    def __init__(self, df: pd.DataFrame, date_column: str = 'Date', location_column: str = None, format = False):

        self.df = df.copy()
        self.date_column = date_column
        self.location_column = location_column if location_column in df.columns else None
        self.format = format
    
    def convert_location(self):
        """
            Para mapas de accidentes con posiciones exactas 
            Extrae Longitud y Latitud del string y las convierte a Series dedicadas

        """
        if not self.location_column:
            print("No hay ubicación de los accidentes, no se hará conversión de posición...")
            return self
        
        lats = []
        longs = []
        # print(self.df[self.location_column].items())
        
        for item in self.df[self.location_column].items():
            s = item[1]
            coord = re.findall(r"[0-9]+\.[0-9]+", s) # Reconoce la exoresión regular para coordenadas cartesianas
            if len(coord) == 2:
                longs.append(float(coord[0]) * -1)  
                lats.append(float(coord[1]))
            else:
                longs.append(None)
                lats.append(None)

        self.df['LATITUDE'] = lats
        self.df['LONGITUDE'] = longs
        self.df.drop(columns=[self.location_column, 'City', 'Avg Reliability'], inplace=True)

        return self
        
    def convert_date(self):
        """
        Conversión total de las cadenas de 12-ene-2024 a objetos date y pd.date
        - 'DatePython' as a datetime object
        - 'Date_numeric' as a Unix timestamp
        """
        if self.format == False:
            month_map = {
                'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
                'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
                'sept': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
            }

            def _replace_months(date_str):
                for esp, eng in month_map.items():
                    if esp in date_str:
                        return date_str.replace(esp, eng)
                return date_str

            self.df['Date_cleaned'] = self.df[self.date_column].apply(_replace_months)
            self.df['DatePython'] = pd.to_datetime(self.df['Date_cleaned'], format='%d %b %Y', errors='coerce')
            self.df['Date_tuple'] = self.df['DatePython'].apply(
                lambda x: x.date() if pd.notnull(x) else None
            )

            return self

        else:

            self.df['DatePython'] = pd.to_datetime(self.df[self.date_column], format='%Y-%m-%d', errors='coerce')
            self.df['Date_tuple'] = self.df['DatePython'].apply(
                lambda x: x.date() if pd.notnull(x) else None
            )

            return self



    
    def addFilters(self):
        """
            Añade series extras que pueden ser utiles para filtros 
        """

        self.df['WeekdayNum'] = self.df['DatePython'].dt.dayofweek
        self.df['Weekday'] = self.df['DatePython'].dt.day_name()
        self.df['Month'] = self.df['DatePython'].dt.month
        self.df['WeekNum'] =self.df['DatePython'].dt.isocalendar().week

        return self

    def get_transformed_df(self):
        return self
    
