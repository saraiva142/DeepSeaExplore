import streamlit as st
from streamlit_folium import st_folium
import folium
from api.obis_api import buscar_ocorrencias_por_area
from api.inaturalist_api import buscar_imagem_especie
from math import radians, cos, sin, sqrt, atan2

st.set_page_config(page_title="Mapa de Espécies", page_icon="🗺️", layout="wide")
st.title("🌍 Mapa de Espécies Marinhas")

# Inputs
lat = st.number_input("Latitude", value=-32.0)
lon = st.number_input("Longitude", value=153.0)
raio = st.slider("Raio da busca (km)", 10, 500, 50)
limite = st.slider("Número máximo de registros", 10, 500, 100)

# Inicializa estado da sessão
if "resultados" not in st.session_state:
    st.session_state.resultados = None

# Botão de busca
if st.button("🔍 Buscar Espécies"):
    st.session_state.resultados = buscar_ocorrencias_por_area(lat, lon, raio, limite)

# Calcula distância entre dois pontos usando a fórmula de Haversine
def distancia_km(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Lista de espécies genéricas a serem ignoradas
blacklist = {"Amoebophrya", "Syndiniales", "Rudilemboides naglei"}

# Mapa inicial com círculo de busca
m = folium.Map(location=[lat, lon], zoom_start=8)
folium.Circle(location=[lat, lon], radius=raio * 1000, color="blue", fill=True, fill_opacity=0.2).add_to(m)

# Filtra e plota os resultados
resultados_validos = []

if st.session_state.resultados:
    for r in st.session_state.resultados:
        ponto_lat = r.get("decimalLatitude")
        ponto_lon = r.get("decimalLongitude")
        especie = r.get("scientificName")

        if not ponto_lat or not ponto_lon or not especie:
            continue

        if especie in blacklist:
            continue

        # Verifica se está dentro do raio desejado
        if distancia_km(lat, lon, ponto_lat, ponto_lon) <= raio:
            resultados_validos.append(r)
            folium.Marker(
                location=[ponto_lat, ponto_lon],
                popup=especie,
                icon=folium.Icon(color="green", icon="leaf"),
            ).add_to(m)

    st.success(f"{len(resultados_validos)} ocorrências dentro da área selecionada.")

# Exibe o mapa
st_folium(m, width=1000, height=600)

# Exibe imagens das espécies encontradas
if resultados_validos:
    st.subheader("🔍 Espécies Encontradas na Área")

    especies_unicas = list({r.get("scientificName") for r in resultados_validos if r.get("scientificName")})
    especies_exibir = especies_unicas[:20]

    for especie in especies_exibir:
        imagem = buscar_imagem_especie(especie)
        if imagem:
            st.image(imagem, caption=especie, width=120)
        else:
            st.write(f"🖼️ Imagem não encontrada para {especie}.")
