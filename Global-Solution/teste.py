import folium
from api import geolocalizacao
import json

with open("Global-Solution/json/outras.json", "r", encoding="latin-1") as file:
    data = json.load(file)

# Coordenadas do usuário
latitude_usuario, longitude_usuario = geolocalizacao.coordenadas_usuario("02346-000", "158")

# Criar o mapa inicial com as coordenadas do usuário
mapa = folium.Map(location=[latitude_usuario, longitude_usuario], zoom_start=10)

# Adicionar marcador para a localização do usuário
folium.Marker([latitude_usuario, longitude_usuario], popup='Minha Localização').add_to(mapa)

# Adicionar marcadores para as clínicas
for d in data["outras"]:
    latitude, longitude = geolocalizacao.coordenadas_hospitais(d)
    
    # Verificar se latitude e longitude são válidas antes de adicionar o marcador
    if latitude is not None and longitude is not None:
        folium.Marker([latitude, longitude], popup=d["nome"]).add_to(mapa)
    else:
        print(f"Coordenadas inválidas para {d['nome']}")

mapa.show_in_browser()
