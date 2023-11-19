import folium
from api import geolocalizacao
from IPython.display import display

latitude, longitude = geolocalizacao.coordenadas("02346-000", "158")

mapa = folium.Map(location=[latitude, longitude], zoom_start=12)

folium.Marker([latitude, longitude], popup='Minha Localização').add_to(mapa)

mapa.show_in_browser()
