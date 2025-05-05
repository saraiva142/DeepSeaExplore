# 🌊 Deep Sea Explorer

![🌐 Streamlit App](https://deepseaexplorer.streamlit.app/)

**Deep Sea Explorer** é uma aplicação interativa desenvolvida em Python com [Streamlit](https://streamlit.io/) para explorar a biodiversidade marinha global. Usando dados de APIs científicas e fontes como OBIS, iNaturalist, EOL e Wikipedia, o app permite investigar espécies oceânicas, visualizar mapas de ocorrências, acessar descobertas curiosas e analisar a diversidade marinha em diferentes regiões.

---

## 🧭 Funcionalidades

- 🔍 **Busca por Área**  
  Insira coordenadas geográficas e um raio para encontrar espécies animais marinhas registradas na região, com base nos dados da OBIS (Ocean Biodiversity Information System).

- 🗺️ **Mapa de Espécies**  
  Visualize interativamente os pontos de ocorrência das espécies encontradas, com nome científico, imagem e link para mais informações.

- 📚 **Informações de Espécies**  
  Integração com Wikipedia e EOL para mostrar um resumo limpo e confiável sobre cada espécie.

- 🧠 **Descobertas Curiosas**  
  Uma seção divertida que apresenta fatos inusitados e interessantes sobre espécies encontradas no oceano.

- 📊 **Análise de Diversidade**  
  Visualizações que mostram a diversidade de espécies por grupo taxonômico, profundidade e outras métricas ecológicas.

---

## 🧪 Tecnologias Utilizadas

- **Python 3**
- [Streamlit](https://streamlit.io/)
- [OBIS API](https://api.obis.org/)
- [iNaturalist API](https://www.inaturalist.org/pages/api+reference)
- [Encyclopedia of Life (EOL) API](https://eol.org/docs/what-is-eol/data-services)
- [Wikipedia API](https://pypi.org/project/wikipedia/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/) para visualizações
- [Folium](https://python-visualization.github.io/folium/) para mapas

---

## 🛠️ Estrutura do Projeto

Directory structure:
└── saraiva142-deepseaexplore/
    ├── main.py
    ├── requirements.txt
    ├── api/
    │   ├── eol_api.py
    │   ├── inaturalist_api.py
    │   ├── obis_api.py
    │   ├── wikipedia_api.py
    │   └── __pycache__/
    ├── assets/
    ├── Home/
    │   ├── overview.py
    │   └── __pycache__/
    └── pages/
        ├── Analise_de_Diversidade.py
        ├── Descobertas_Curiosas.py
        └── Mapa_de_Especies.py

---

## 🚀 Como Rodar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/deep-sea-explorer.git
   cd deep-sea-explorer

2. Crie um ambiente virtual e instale as dependências:
```python -m venv venv```
```source venv/bin/activate  # ou venv\Scripts\activate no Windows ```
```pip install -r requirements.txt```

3. Rode a aplicação:
```streamlit run main.py```

## 🐠 Exemplos de Uso 
* Investigar a biodiversidade ao redor das Ilhas Galápagos

* Descobrir espécies misteriosas em áreas profundas do oceano

* Visualizar quais animais marinhos ocorrem em sua região costeira

* Aprender curiosidades sobre criaturas marinhas exóticas

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests.