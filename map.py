import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("Primer Mapa - Alrededor de Morelia")

df = pd.read_csv("/Users/juanmagonzalez/VsCode/streamlit/first/Accidentes_Morelia.csv")

st.map(df, size=10)

# coordinates = df.loc[:,["Latitude", "Longitude"]]
# st.session_state.points = coordinates



# # Pydeck layer and view
# layer = pdk.Layer(
#     "ScatterplotLayer",
#     st.session_state.points,
#     get_position='[Longitude, Latitude]',
#     get_color='[0, 100, 250, 160]',
#     get_radius=20,
# )

# view_state = pdk.ViewState(
#     latitude=20.659698,
#     longitude=-103.349609,
#     zoom=12,
#     pitch=0,
# )

# st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
