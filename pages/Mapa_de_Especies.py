import streamlit as st
from streamlit_folium import st_folium
import folium
from api.obis_api import buscar_ocorrencias_por_area
from api.inaturalist_api import buscar_imagem_especie
from math import radians, cos, sin, sqrt, atan2

st.set_page_config(page_title="Mapa de Espécies", page_icon="🗺️", layout="wide")
st.title("🌍 Mapa de Espécies Marinhas")

# Localizações pré-definidas
paises = {
    "Brasil": {"lat": -23.0, "lon": -43.0},
    "Austrália": {"lat": -32.0, "lon": 153.0},
    "África do Sul": {"lat": -35.0, "lon": 18.0},
    "Indonésia": {"lat": -5.0, "lon": 120.0},
    "Canadá": {"lat": 49.0, "lon": -64.0},
    "Reino Unido": {"lat": 51.5, "lon": -0.1},
    "Estados Unidos": {"lat": 34.0, "lon": -119.0},
    "Nova Zelândia": {"lat": -41.0, "lon": 174.0},
    "França": {"lat": 46.0, "lon": 2.0},
    "Noruega": {"lat": 60.0, "lon": 8.0},
    "Japão": {"lat": 36.0, "lon": 138.0},
    "Portugal": {"lat": 41.0, "lon": -9.0},
    "Mundo todo": {"lat": 0.0, "lon": 0.0},
}

# Tipo de entrada
opcao = st.radio("Escolha como deseja inserir os dados:", ("Manual", "Por País"))

# Coordenadas default -> Da lá na costa sudeste da Austrália
if "lat" not in st.session_state:
    st.session_state.lat = -32.0
if "lon" not in st.session_state:
    st.session_state.lon = 153.0

if opcao == "Manual":
    lat = st.number_input("Latitude", value=st.session_state.lat, key="input_lat")
    lon = st.number_input("Longitude", value=st.session_state.lon, key="input_lon")
else:
    pais = st.selectbox("Escolha um país:", list(paises.keys()))
    lat = paises[pais]["lat"]
    lon = paises[pais]["lon"]
    st.session_state.lat = lat
    st.session_state.lon = lon
    st.write(f"Coordenadas selecionadas: Latitude {lat}, Longitude {lon}")

# Atualiza os valores da sessão
st.session_state.lat = lat
st.session_state.lon = lon

# Raio e limite
raio = st.slider("Raio da busca (km)", 10, 500, 50)
limite = st.slider("Número máximo de registros", 50, 5000, 1000)

# Botão para buscar
if st.button("🔍 Buscar Espécies"):
    st.session_state.resultados = buscar_ocorrencias_por_area(lat, lon, raio, limite)

# Haversine -> Distância entre dois pontos na superfície da Terra
def distancia_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 🔍 Blacklist
blacklist = {"Amoebophrya", "Syndiniales", "Rudilemboides naglei"}

# Mapa interativo (inicial) -> Fazer ele mais iterativo foi ideia da Clara
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=8)
folium.Circle([st.session_state.lat, st.session_state.lon], radius=raio*1000,
              color="blue", fill=True, fill_opacity=0.2).add_to(m)

# Mostrar dados anteriores (após clique no botão)
resultados_validos = []
if st.session_state.get("resultados"):
    for r in st.session_state.resultados:
        ponto_lat = r.get("decimalLatitude")
        ponto_lon = r.get("decimalLongitude")
        especie = r.get("scientificName")

        if not ponto_lat or not ponto_lon or not especie:
            continue
        if especie in blacklist:
            continue
        if distancia_km(st.session_state.lat, st.session_state.lon, ponto_lat, ponto_lon) > raio:
            continue

        resultados_validos.append(r)
        
        #Mostrando referências no popup-> Aviso da Clara

        dataset = r.get("datasetName", "Desconhecido")
        licenca = r.get("license", "Licença não informada")
        instituicao = r.get("rightsHolder", "Instituição não informada")
        instituicao_code = r.get("institutionCode", "Código não informado")
        dono_instituicao = r.get("ownerInstitutionCode")

        popup_texto = f"""
        <b>{especie}</b><br>
        <i>Fonte:</i> {dataset}<br>
        <i>Instituição:</i> {instituicao}<br>
        <i>InstituiçãoCode:</i> {instituicao_code}<br>
        <i>Licença:</i> {licenca}
        """
        folium.Marker(
            location=[ponto_lat, ponto_lon],
            popup=folium.Popup(popup_texto, max_width=250),
            icon=folium.Icon(color="green", icon="leaf")
        ).add_to(m)

    st.success(f"{len(resultados_validos)} ocorrências dentro da área selecionada.")

# Mapa interativo final
output = st_folium(m, width=1000, height=600)

# Atualiza lat/lon apenas no clique (sem atualizar resultado)
if output.get("last_clicked"):
    st.session_state.lat = output["last_clicked"]["lat"]
    st.session_state.lon = output["last_clicked"]["lng"]
    st.success(f"📍 Coordenadas selecionadas no mapa: ({st.session_state.lat:.4f}, {st.session_state.lon:.4f}) " )
    
    if st.button("🔍 Buscar Espécies Com Novas Coordenadas"):
        st.session_state.resultados = buscar_ocorrencias_por_area(lat, lon, raio, limite)

# Imagens -> Mostrando referências -> Aviso da Clara
if resultados_validos:
    st.subheader("🔍 Espécies Encontradas na Área")
    especies_unicas = list({r.get("scientificName") for r in resultados_validos if r.get("scientificName")})
    for especie in especies_unicas[:100]:
        imagem = buscar_imagem_especie(especie)
        registro = next((r for r in resultados_validos if r.get("scientificName") == especie), None)
        col1, col2 = st.columns([1, 3])
        with col1:
            if imagem:
                st.image(imagem, caption=especie, width=120)
            else:
                st.image("https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
                         caption=especie, width=120)

        with col2:
            if registro:
                dataset = registro.get('datasetName')
                instituicao_code = registro.get("institutionCode")
                license = registro.get("license")
            else:
                dataset = "Desconhecido"
                instituicao_code = "Desconhecida"
                license = "Licença não informada"
            st.markdown(f"**📁 Dataset:** {dataset}")
            st.markdown(f"**🏛️ Instituição:** {instituicao_code}")
            st.markdown(f"**📜 Licença:** {license}")
            # st.markdown(f"**🏛️ Instituição:** {r.get('institutionCode', 'Desconhecida')}") Ta dando sempre desconhecido

        st.markdown("---")
