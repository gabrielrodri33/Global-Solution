import json
from geopy.geocoders import Nominatim
from api import viacep
from geopy.exc import GeocoderTimedOut

def coordenadas_usuario(cep, numero):
    localizacao = viacep.cep(cep)

    geolocalizaco = Nominatim(user_agent="teste")

    endereco_completo = f"{localizacao['logradouro']}, {numero}, {localizacao['localidade']} - {localizacao['bairro']}"

    localizacao = geolocalizaco.geocode(endereco_completo)

    return str(localizacao.latitude), str(localizacao.longitude)

from geopy.exc import GeocoderTimedOut

def coordenadas_hospitais(data):
    geolocalizacao = Nominatim(user_agent="teste")

    endereco_completo = f'{data["endereco"]}, {data["cidade"]}, {data["estado"]}'
    endereco_completo = endereco_completo.encode('latin-1').decode("utf-8")
    print(endereco_completo)

    try:
        localizacao = geolocalizacao.geocode(endereco_completo)
        if localizacao:
            return localizacao.latitude, localizacao.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        print(f"O geocodificador excedeu o tempo para o endereço: {endereco_completo}")
        return None, None
