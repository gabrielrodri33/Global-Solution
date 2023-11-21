from geopy.geocoders import Nominatim
from api import viacep
from geopy.exc import GeocoderTimedOut

def coordenadas_usuario(cep, numero):
    localizacao = viacep.cep(cep)

    geolocalizaco = Nominatim(user_agent="teste")

    endereco_completo = f"{localizacao['logradouro']}, {numero}, {localizacao['localidade']} - {localizacao['bairro']}"

    localizacao = geolocalizaco.geocode(endereco_completo)

    return str(localizacao.latitude), str(localizacao.longitude)

def coordenadas_hospitais(data):
    geolocalizacao = Nominatim(user_agent="teste")

    endereco_completo = f'{data["endereco"]}, {data["cidade"]}, {data["estado"]}'

    try:
        localizacao = geolocalizacao.geocode(endereco_completo, timeout=60)
        if localizacao:
            return localizacao.latitude, localizacao.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        print(f"O geocodificador excedeu o tempo para o endereço: {endereco_completo}")
        return None, None
