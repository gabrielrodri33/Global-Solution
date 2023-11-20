import folium
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api import geolocalizacao

def localizacoes(json_name, value):
    file = f"Global-Solution/json/{json_name}.json"
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)

    latitude_usuario, longitude_usuario = geolocalizacao.coordenadas_usuario("02346-000", "158")

    mapa = folium.Map(location=[latitude_usuario, longitude_usuario], zoom_start=10)

    folium.Marker([latitude_usuario, longitude_usuario], popup='Minha Localização', icon=folium.Icon(color='red')).add_to(mapa)

    for d in data[value]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(d)
        
        if latitude is not None and longitude is not None:
            folium.Marker([latitude, longitude], popup=d["nome"]).add_to(mapa)
        else:
            print(f"Coordenadas inválidas para {d['nome']}")

    mapa_name = f"Global-Solution/html/{json_name}.html"

    mapa.save(mapa_name)

def localizacao_clinicas():
    with open("Global-Solution/json/hospitais.json", "r", encoding="latin-1") as file:
        data = json.load(file)
    
    latitude_usuario, longitude_usuario = geolocalizacao.coordenadas_usuario("02346-000", "158")
    mapa = folium.Map(location=[latitude_usuario, longitude_usuario], zoom_start=10)

    folium.Marker([latitude_usuario, longitude_usuario], popup='Minha Localização').add_to(mapa)

    for d in data["hospital"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(d)
        
        if latitude is not None and longitude is not None:
            folium.Marker([latitude, longitude], popup=d["nome"]).add_to(mapa)
        else:
            print(f"Coordenadas inválidas para {d['nome']}")

    mapa.show_in_browser()

def principal():
    localizacoes("outras", "outras")
    localizacoes("clinica", "clinicas")
    localizacoes("hospitais", "hospital")
    localizacoes("imagemlaboratorio", "imagemlaboratorio")
    localizacoes("pa", "prontoatendimento")

#Programa Principal
principal()