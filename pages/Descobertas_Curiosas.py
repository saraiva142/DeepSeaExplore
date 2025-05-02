import streamlit as st
import pandas as pd
import random
from api.obis_api import buscar_ocorrencias_por_area
from api.inaturalist_api import buscar_imagem_especie

st.set_page_config(page_title="Descobertas Curiosas", page_icon="🔍", layout="wide")
st.title("🔍 Descobertas Curiosas do Fundo do Mar")

# 🧠 Palavras curiosas para filtrar nomes
palavras_chave = [
    "salmo trutta", "copepoda", "decapoda", "surirella", "hydrozoa", "salmo salar", "avicennia",
    "mammalia", "kolga nana", "fiona", "tripos dens", "sebastes", "delphinus delphis", "calanoida", "oceanodroma"
]

# 🔄 Gera uma busca aleatória ao redor do mundo
lat_aleatoria = random.uniform(-60, 60)
lon_aleatoria = random.uniform(-180, 180)
raio = 100000
limite = 1000

st.info("Explorando o oceano em busca de criaturas curiosas...")

# Busca registros globais aleatórios
resultados = buscar_ocorrencias_por_area(lat_aleatoria, lon_aleatoria, raio, limite)

# Filtra registros com nomes curiosos
curiosas = []
for r in resultados:
    nome = r.get("scientificName", "").lower()
    nome_original = r.get("originalScientificName", "").lower()

    if any(p in nome for p in palavras_chave) or any(p in nome_original for p in palavras_chave):
        curiosas.append(r)
    # else:
    #     st.write(f"Nome ignorado: {nome}")

# Elimina duplicatas por nome científico
vistos = set()
curiosas_unicas = []
for c in curiosas:
    nome = c.get("scientificName")
    if nome and nome not in vistos:
        curiosas_unicas.append(c)
        vistos.add(nome)

if curiosas_unicas:
    st.success(f"🌊 Encontramos {len(curiosas_unicas)} criaturas curiosas!")

    # Seleciona uma criatura curiosa aleatoriamente
    criatura_aleatoria = random.choice(curiosas_unicas)

    nome = criatura_aleatoria.get("scientificName", "Espécie desconhecida")
    imagem = buscar_imagem_especie(nome)

    st.subheader(f"🧬 {nome.title()}")

    col1, col2 = st.columns([1, 3])
    with col1:
        if imagem:
            st.image(imagem, width=150)
        else:
            st.image("https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg", width=150)
    with col2:
        st.markdown("**Espécie curiosa detectada!**")
        st.markdown(f"`{nome}`")
        st.caption("🔍 Esta espécie possui algo interessante ou algo ainda mais bizarro.")
        st.divider()
else:
    st.warning("😢 Nenhuma criatura curiosa foi encontrada desta vez. Tente novamente atualizando a página.")