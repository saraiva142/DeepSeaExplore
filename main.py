import streamlit as st
from Home import overview

def DeepSeaExplore():
    
    st.set_page_config(
        page_title="DeepSea Explorer",
        page_icon="🌊",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Barra lateral com navegação
    #st.sidebar.title("🔎 Navegação")

    # Corpo da página
    st.title("🌊 DeepSea Explorer")
    overview.mostrar_overview()

pg = st.navigation([DeepSeaExplore, "./pages/Mapa_de_Especies.py", "./pages/teste_mapa.py"])
pg.run()