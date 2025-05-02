import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Teste Mapa", layout="wide")

st.title("🧪 Teste de Mapa Folium Simples")

lat = -12.97
lon = -38.51

m = folium.Map(location=[lat, lon], zoom_start=8)
folium.Marker(location=[lat, lon], popup="Salvador").add_to(m)

st_folium(m, width=1000, height=600)
