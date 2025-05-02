import streamlit as st

def mostrar_overview():
    st.header("📘 Sobre o Projeto")
    st.markdown("""
    O **DeepSea Explorer** é uma ferramenta educacional e científica desenvolvida com Python e Streamlit, 
    que permite visualizar espécies marinhas registradas ao redor do mundo.

    **Funcionalidades principais:**
    - 🌍 Mapa interativo com espécies registradas por localização
    - 📊 Gráficos de diversidade ao longo do tempo
    - 🧬 Modo “Descobertas Curiosas”
    - 🌌 Modo “Noite Marinha”
    - 🎙️ (em breve) Comandos por voz usando Whisper

    ---
    Explore, aprenda e se encante com a biodiversidade subaquática!
    """)
