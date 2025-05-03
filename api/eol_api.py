import requests

def buscar_descricao_eol(nome_cientifico, idioma="pt"):
    try:
        url_busca = f"https://eol.org/api/search/1.0.json?q={nome_cientifico}"
        r = requests.get(url_busca)
        resultados = r.json().get("results", [])

        if not resultados:
            return {"erro": f"Nenhum resultado EOL para {nome_cientifico}"}

        # Pega o primeiro ID
        id_eol = resultados[0]["id"]
        url_conteudo = f"https://eol.org/api/pages/1.0/{id_eol}.json?details=true&language={idioma}"

        resposta = requests.get(url_conteudo)
        dados = resposta.json()

        for item in dados.get("dataObjects", []):
            if item.get("description"):
                return {
                    "titulo": nome_cientifico,
                    "resumo": item["description"],
                    "url": f"https://eol.org/pages/{id_eol}"
                }

        return {"erro": "Descrição não encontrada na EOL."}
    except Exception as e:
        return {"erro": f"Erro na API da EOL: {str(e)}"}
