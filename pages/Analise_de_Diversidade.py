import streamlit as st
import plotly.express as px
import pandas as pd
from api.obis_api import buscar_ocorrencias_por_area
from math import radians, cos, sin, sqrt, atan2

st.set_page_config(page_title="Análise de Diversidade", page_icon="📈", layout="wide")
st.title("📈 Análise de Diversidade de Espécies")

# 📍 Localizações pré-definidas
paises = {
    "Brasil": {"lat": -23.0, "lon": -43.0, "raio": 300},
    "Austrália": {"lat": -32.0, "lon": 153.0, "raio": 300},
    "África do Sul": {"lat": -35.0, "lon": 18.0, "raio": 300},
    "Indonésia": {"lat": -5.0, "lon": 120.0, "raio": 300},
    "Canadá": {"lat": 49.0, "lon": -64.0, "raio": 300},
    "Reino Unido": {"lat": 51.5, "lon": -0.1, "raio": 300},
    "Estados Unidos": {"lat": 34.0, "lon": -119.0, "raio": 300},
    "Nova Zelândia": {"lat": -41.0, "lon": 174.0, "raio": 300},
    "França": {"lat": 46.0, "lon": 2.0, "raio": 300},
    "Noruega": {"lat": 60.0, "lon": 8.0, "raio": 300},
    "Japão": {"lat": 36.0, "lon": 138.0, "raio": 300},
    "Portugal": {"lat": 41.0, "lon": -9.0, "raio": 300},
    "Mundo todo": {"lat": 0.0, "lon": 0.0, "raio": 15000}
}

# 🌍 Seleção de região
pais_selecionado = st.selectbox("Escolha uma região para análise:", list(paises.keys()))
config = paises[pais_selecionado]

limite = st.slider("Número máximo de registros", 50, 5000, 1000)

# 📏 Fórmula de Haversine para filtro por raio real
def distancia_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 🔘 Botão para iniciar análise
if st.button("📊 Analisar Diversidade"):
    st.info(f"Buscando dados da região: {pais_selecionado}...")
    resultados = buscar_ocorrencias_por_area(config["lat"], config["lon"], config["raio"], limite)

    # 🔹 Filtra os dados por distância real
    dados_filtrados = []
    for r in resultados:
        lat_oc = r.get("decimalLatitude")
        lon_oc = r.get("decimalLongitude")
        if not lat_oc or not lon_oc:
            continue
        if distancia_km(config["lat"], config["lon"], lat_oc, lon_oc) <= config["raio"]:
            dados_filtrados.append(r)

    st.info(f"🔎 {len(dados_filtrados)} registros encontrados dentro do raio.")

    if not dados_filtrados:
        st.warning("Nenhum dado encontrado dentro do raio selecionado.")
    else:
        df = pd.DataFrame(dados_filtrados)

        st.success(f"{len(df)} registros encontrados para análise.")

        st.write("📄 Amostra dos dados:")
        st.dataframe(df[["scientificName"]].head(10))
        st.write("📊 Quantidade de espécies únicas:", df["scientificName"].nunique())

        # 🥧 Gráfico de pizza com as espécies mais frequentes
        contagem = df["scientificName"].value_counts()
        top_especies = contagem[contagem > 1].head(10).reset_index()
        top_especies.columns = ["Espécie", "Ocorrências"]

        if not top_especies.empty:
            fig_pizza = px.pie(top_especies, names="Espécie", values="Ocorrências",
                               title="Top 10 Espécies Mais Registradas",
                               hole=0.4)
            st.plotly_chart(fig_pizza, use_container_width=True)
        else:
            st.warning("Não há espécies com múltiplas ocorrências suficientes para gerar o gráfico de pizza.")

        # 📈 Gráfico temporal (somente se houver ano)
        if "year" in df.columns and df["year"].notna().sum() > 0:
            df_com_ano = df[df["year"].notna()]
            df_com_ano["year"] = df_com_ano["year"].astype(int)
            df_com_ano = df_com_ano[df_com_ano["year"] >= 1880]  # Filtra anos irreais, pois tinha ano 0 aqui kkkk

            diversidade_ano = (
                df_com_ano.groupby("year")["scientificName"]
                .nunique()
                .reset_index()
                .rename(columns={"scientificName": "Espécies únicas"})
            )

            fig_linha = px.line(diversidade_ano, x="year", y="Espécies únicas",
                                title="Diversidade ao Longo do Tempo",
                                markers=True)
            fig_linha.update_layout(xaxis_title="Ano", yaxis_title="Espécies Únicas")
            st.plotly_chart(fig_linha, use_container_width=True)
        else:
            st.info("ℹ️ Nenhum dos registros possui informação de ano. Gráfico temporal não será exibido.")

        # 📋 Tabela completa (expansível)
        with st.expander("📄 Ver tabela de dados brutos"):
            colunas = ["scientificName", "decimalLatitude", "decimalLongitude"]
            if "year" in df.columns:
                colunas.insert(1, "year")  # insere 'year' após 'scientificName'
            st.dataframe(df[colunas])

