import requests
import random

OBIS_BASE_URL = "https://api.obis.org/v3/occurrence"

def buscar_ocorrencias_por_area(lat, lon, raio_km, limite=10000):
    try:
        # Converte o raio de km para graus (aproximado: 1 grau ≈ 111 km)
        delta = raio_km / 111.0

        min_lat = lat - delta
        max_lat = lat + delta
        min_lon = lon - delta
        max_lon = lon + delta

        # offset = random.randint(0, 3000)
        offset = 0
        
        url = (
            f"{OBIS_BASE_URL}?"
            f"decimalLatitude>={min_lat}&decimalLatitude<={max_lat}"
            f"&decimalLongitude>={min_lon}&decimalLongitude<={max_lon}"
            #f"&kingdom=Animalia"
            f"&hasCoordinate=true"
            # f"&hasDepth=true"
            f"&size={limite}&offset={offset}"
        )
        
        print(f"🔍 URL usada: {url}")
        print(f"🌍 Latitude: {lat}, Longitude: {lon}, Raio (km): {raio_km}")
        print(f"🟡 Requisição enviada...")

        response = requests.get(url)
        print(f"✅ Status code: {response.status_code}")
        #print(f"📦 Dados recebidos: {response.json()}")
        response.raise_for_status()
        dados = response.json()
        return dados.get("results", [])
    except Exception as e:
        print(f"Erro ao buscar dados da OBIS: {e}")
        return []

