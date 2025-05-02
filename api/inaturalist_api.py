import requests

def buscar_imagem_especie(nome_cientifico):
    url = "https://api.inaturalist.org/v1/search"
    params = {
        "q": nome_cientifico,
        "sources": "taxa",
        "per_page": 1,
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        dados = resp.json()
        if dados["results"]:
            taxon = dados["results"][0].get("record", {})
            default_photo = taxon.get("default_photo")
            if default_photo:
                return default_photo.get("medium_url")
            else:
                print(f"Imagem não encontrada para {nome_cientifico}.")
            #return taxon.get("default_photo", {}).get("medium_url")
    return None