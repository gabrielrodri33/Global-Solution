import requests

def cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json'
    
    requisicao = requests.get(url)

    dic = requisicao.json()

    return dic