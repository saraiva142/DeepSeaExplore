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
    st.title("DeepSea Explorer")
    st.image("./assets/banner.png", width=700)
    overview.mostrar_overview()
    
    st.markdown(
        """
        <style>
        .footer {
            position: relative;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 12px;
            color: gray;
            padding: 10px 0;
            margin-top: 50px;
        }
        </style>
        <div class="footer">
            Desenvolvido por João Saraiva 👨‍💻
        </div>
        """,
        unsafe_allow_html=True
    )

pg = st.navigation([DeepSeaExplore, "./pages/Mapa_de_Especies.py", "./pages/Analise_de_Diversidade.py"])
pg.run()