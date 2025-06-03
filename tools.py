import pandas as pd
from datetime import date

class dfTransform:
    def __init__(self, df, format):
        self.df = df
        if format == True:
            self.df['DatePython'] = pd.to_datetime(self.df['Date'], format='%Y-%m-%d')
            
    def convert(self, format):
        if format == True:
            self.df['Date'] = pd.to_datetime(self.df['Date'], format='%Y-%m-%d').dt.date

    def addFilters(self):
        self.df['WeekdayNum'] = self.df['DatePython'].dt.dayofweek
        self.df['Weekday'] = self.df['DatePython'].dt.day_name()
        self.df['Month'] = self.df['DatePython'].dt.month
        self.df['WeekNum'] =self.df['DatePython'].dt.isocalendar().week

        return self.df


# def convert(df):