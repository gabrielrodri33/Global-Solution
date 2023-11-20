import folium
from api import geolocalizacao
import json

#https://www.hapvida.com.br/site/rede-exclusiva

def localizacoes_outras():
    with open("Global-Solution/json/outras.json", "r", encoding="latin-1") as file:
        data = json.load(file)

    latitude_usuario, longitude_usuario = geolocalizacao.coordenadas_usuario("02346-000", "158")

    mapa = folium.Map(location=[latitude_usuario, longitude_usuario], zoom_start=10)

    folium.Marker([latitude_usuario, longitude_usuario], popup='Minha Localização').add_to(mapa)

    for d in data["outras"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(d)
        
        if latitude is not None and longitude is not None:
            folium.Marker([latitude, longitude], popup=d["nome"]).add_to(mapa)
        else:
            print(f"Coordenadas inválidas para {d['nome']}")

    mapa.show_in_browser("outras.html")

localizacoes_outras()
