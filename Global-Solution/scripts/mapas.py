import folium
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api import geolocalizacao

# https://www.hapvida.com.br/site/rede-exclusiva
# https://www.gndi.com.br/unidades

def link_hospital(data):
    latitude, longitude = geolocalizacao.coordenadas_hospitais(data)

    return latitude, longitude

def localizacoes(json_name, value, cep, numero):
    file = f"Global-Solution/json/{json_name}.json"
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)

    latitude_usuario, longitude_usuario = geolocalizacao.coordenadas_usuario(cep, numero)

    mapa = folium.Map(location=[latitude_usuario, longitude_usuario], zoom_start=10)

    folium.Marker([latitude_usuario, longitude_usuario], popup='Minha Localização', icon=folium.Icon(color='red')).add_to(mapa)

    for d in data[value]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(d)
        
        if latitude is not None and longitude is not None:
            popup_content = f"{d['nome']}<br><a href='https://www.google.com/maps/place/{latitude},{longitude}' target='_blank'>Ver no Google Maps</a>"
            folium.Marker([latitude, longitude], popup=popup_content).add_to(mapa)
        else:
            # print(f"Coordenadas inválidas para {d['nome']}")
            pass

    mapa_name = f"Global-Solution/html/{json_name}.html"

    mapa.save(mapa_name)

    return data

def todas_localizacoes(json_name, value, outras, clinica, hospitais, imagem, pa, cep, numero):
    file = f"Global-Solution/json/{json_name}.json"
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)

    latitude_usuario, longitude_usuario = geolocalizacao.coordenadas_usuario(cep, numero)

    mapa = folium.Map(location=[latitude_usuario, longitude_usuario], zoom_start=10)

    folium.Marker([latitude_usuario, longitude_usuario], popup='Minha Localização', icon=folium.Icon(color='red')).add_to(mapa)

    for d in data[value]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(d)
        
        if latitude is not None and longitude is not None:
            popup_content = f"{d['nome']}<br><a href='https://www.google.com/maps/place/{latitude},{longitude}' target='_blank'>Ver no Google Maps</a>"
            folium.Marker([latitude, longitude], popup=popup_content).add_to(mapa)
        else:
            # print(f"Coordenadas inválidas para {d['nome']}")
            pass

    for o in outras["outras"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(o)
        if latitude is not None and longitude is not None:
            popup_content = f"{o['nome']}<br><a href='https://www.google.com/maps/place/{latitude},{longitude}' target='_blank'>Ver no Google Maps</a>"
            folium.Marker([latitude, longitude], popup=popup_content, icon=folium.Icon(color='green')).add_to(mapa)
        else:
            # print(f"Coordenadas inválidas para {o['nome']}")
            pass

    for c in clinica["clinicas"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(c)
        
        if latitude is not None and longitude is not None:
            popup_content = f"{c['nome']}<br><a href='https://www.google.com/maps/place/{latitude},{longitude}' target='_blank'>Ver no Google Maps</a>"
            folium.Marker([latitude, longitude], popup=popup_content, icon=folium.Icon(color='purple')).add_to(mapa)
        else:
            # print(f"Coordenadas inválidas para {c['nome']}")
            pass

    for h in hospitais["hospital"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(h)
        
        if latitude is not None and longitude is not None:
            popup_content = f"{h['nome']}<br><a href='https://www.google.com/maps/place/{latitude},{longitude}' target='_blank'>Ver no Google Maps</a>"
            folium.Marker([latitude, longitude], popup=popup_content, icon=folium.Icon(color='orange')).add_to(mapa)
        else:
            # print(f"Coordenadas inválidas para {h['nome']}")
            pass

    for i in imagem["imagemlaboratorio"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(i)
        
        if latitude is not None and longitude is not None:
            popup_content = f"{i['nome']}<br><a href='https://www.google.com/maps/place/{latitude},{longitude}' target='_blank'>Ver no Google Maps</a>"
            folium.Marker([latitude, longitude], popup=popup_content, icon=folium.Icon(color='darkred')).add_to(mapa)
        else:
            # print(f"Coordenadas inválidas para {i['nome']}")
            pass
    
    for p in pa["prontoatendimento"]:
        latitude, longitude = geolocalizacao.coordenadas_hospitais(p)
        
        if latitude is not None and longitude is not None:
            popup_content = f"{p['nome']}<br><a href='https://www.google.com/maps/place/{latitude},{longitude}' target='_blank'>Ver no Google Maps</a>"
            folium.Marker([latitude, longitude], popup=popup_content, icon=folium.Icon(color='cadetblue')).add_to(mapa)
        else:
            # print(f"Coordenadas inválidas para {i['nome']}")
            pass

    mapa_name = f"Global-Solution/html/todos.html"

    mapa.save(mapa_name)

def principal(cep, numero):
    outras = localizacoes("outras", "outras", cep, numero)
    clinica = localizacoes("clinica", "clinicas", cep, numero)
    hospitais = localizacoes("hospitais", "hospital", cep, numero)
    imagem = localizacoes("imagemlaboratorio", "imagemlaboratorio", cep, numero)
    pa = localizacoes("pa", "prontoatendimento", cep, numero)
    todas_localizacoes("notredame", "unidades", outras, clinica, hospitais, imagem, pa, cep, numero)

# Programa Principal

# principal('02345-000', '158')