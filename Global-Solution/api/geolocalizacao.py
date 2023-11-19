from geopy.geocoders import Nominatim
from api import viacep

def coordenadas(cep, numero):
    localizacao = viacep.cep(cep)

    geolocalizaco = Nominatim(user_agent="teste")

    endereco_completo = f"{localizacao['logradouro']}, {numero}, {localizacao['localidade']} - {localizacao['bairro']}"

    localizacao = geolocalizaco.geocode(endereco_completo)

    return str(localizacao.latitude), str(localizacao.longitude)

# latitude, longitude = coordenadas('02346-000')
