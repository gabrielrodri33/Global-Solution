import folium
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api import geolocalizacao

# https://www.hapvida.com.br/site/rede-exclusiva
# https://www.gndi.com.br/unidades

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

def todas_localizacoes(json_name, value, outras, clinica, hospitais, imagem, pa):
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

    for o in outras["outras"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(o)
        if latitude is not None and longitude is not None:
            folium.Marker([latitude, longitude], popup=o["nome"], icon=folium.Icon(color='green')).add_to(mapa)
        else:
            print(f"Coordenadas inválidas para {o['nome']}")

    for c in clinica["clinicas"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(c)
        
        if latitude is not None and longitude is not None:
            folium.Marker([latitude, longitude], popup=c["nome"], icon=folium.Icon(color='purple')).add_to(mapa)
        else:
            print(f"Coordenadas inválidas para {c['nome']}")

    for h in hospitais["hospital"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(h)
        
        if latitude is not None and longitude is not None:
            folium.Marker([latitude, longitude], popup=h["nome"], icon=folium.Icon(color='orange')).add_to(mapa)
        else:
            print(f"Coordenadas inválidas para {h['nome']}")

    for i in imagem["imagemlaboratorio"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(i)
        
        if latitude is not None and longitude is not None:
            folium.Marker([latitude, longitude], popup=i["nome"], icon=folium.Icon(color='darkred')).add_to(mapa)
        else:
            print(f"Coordenadas inválidas para {i['nome']}")
    
    for p in pa["prontoatendimento"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(p)
        
        if latitude is not None and longitude is not None:
            folium.Marker([latitude, longitude], popup=p["nome"], icon=folium.Icon(color='cadetblue')).add_to(mapa)
        else:
            print(f"Coordenadas inválidas para {i['nome']}")

    mapa_name = f"Global-Solution/html/todos.html"

    mapa.save(mapa_name)

def principal():
    outras = localizacoes("outras", "outras")
    clinica = localizacoes("clinica", "clinicas")
    hospitais = localizacoes("hospitais", "hospital")
    imagem = localizacoes("imagemlaboratorio", "imagemlaboratorio")
    pa = localizacoes("pa", "prontoatendimento")
    todas_localizacoes("notredame", "unidades", outras, clinica, hospitais, imagem, pa)

#Programa Principal
principal()