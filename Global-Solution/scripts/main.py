import folium
from api import geolocalizacao
from IPython.display import display
import json

with open("Global-Solution/json/outras.json", "r") as file:
    data = json.load(file)

for d in data["outras"]:
    print(d)

latitude, longitude = geolocalizacao.coordenadas("02346-000", "158")

mapa = folium.Map(location=[latitude, longitude], zoom_start=12)

folium.Marker([latitude, longitude], popup='Minha Localização').add_to(mapa)

mapa.show_in_browser()
