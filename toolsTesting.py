from tools import DataFrameCleanUp
import pandas as pd

df = pd.read_csv("Misc/Jamaica_accidentes_prueba.csv")

transformer = (
    DataFrameCleanUp(df, location_column='Location')
    .convert_location()
    .convert_date()
    .addFilters()

)

clean_df = transformer.get_transformed_df()
clean_df.df.to_csv("Jamaica_cleaned.csv", index=False)