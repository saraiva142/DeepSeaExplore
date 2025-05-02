import streamlit as st
from streamlit_folium import st_folium
import folium
from api.obis_api import buscar_ocorrencias_por_area

st.set_page_config(page_title="Mapa de Espécies", page_icon="🗺️", layout="wide")
st.title("🌍 Mapa de Espécies Marinhas")

# Inputs
lat = st.number_input("Latitude", value=-32)
lon = st.number_input("Longitude", value=153)
raio = st.slider("Raio da busca (km)", 10, 500, 50)
limite = st.slider("Número máximo de registros", 10, 500, 100)

# Inicializa o estado, se necessário
if "resultados" not in st.session_state:
    st.session_state.resultados = None

# Botão que apenas define um gatilho
if st.button("🔍 Buscar Espécies"):
    st.session_state.resultados = buscar_ocorrencias_por_area(lat, lon, raio, limite)

# Agora renderiza o mapa com base no estado
m = folium.Map(location=[lat, lon], zoom_start=8)
folium.Circle(location=[lat, lon], radius=raio * 1000, color="blue", fill=True, fill_opacity=0.2).add_to(m)

# Se há resultados, adiciona ao mapa
if st.session_state.resultados:
    resultados_validos = [
        r for r in st.session_state.resultados
        if isinstance(r.get("decimalLatitude"), (int, float))
        and isinstance(r.get("decimalLongitude"), (int, float))
        and -90 <= r["decimalLatitude"] <= 90
        and -180 <= r["decimalLongitude"] <= 180
        and "ON_LAND" not in r.get("flags", [])
    ]

    st.success(f"{len(resultados_validos)} ocorrências com coordenadas encontradas.")

    for r in resultados_validos:
        ponto_lat = r["decimalLatitude"]
        ponto_lon = r["decimalLongitude"]
        especie = r.get("scientificName", "Espécie desconhecida")

        folium.Marker(
            location=[ponto_lat, ponto_lon],
            popup=especie,
            icon=folium.Icon(color="green", icon="leaf"),
        ).add_to(m)

# Renderiza o mapa (sempre aparece)
st_folium(m, width=1000, height=600)
