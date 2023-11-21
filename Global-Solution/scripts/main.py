import re
import webbrowser
import datetime
import json
import crud
import os
import getpass
import base64
import bcrypt
from api import cellerecpf
from api import viacep

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def separador(n, cor):
    cores = {
        1: {'azul': '\033[36m', 'limpa' : '\033[0m'},
        2: {'verde': '\033[32m', 'limpa' : '\033[0m'},
        3: {'roxo' : '\033[95m' , 'limpa' : '\033[0m'},
        4: {'amarelo': '\033[33m', 'limpa': '\033[0m'},
        5: {'vermelho': '\033[31m', 'limpa': '\033[0m'}
    }

    if cor == 1:
        mensagem = f'{cores[1]["azul"]}-={cores[1]["limpa"]}' * n

    elif cor == 2:
        mensagem = f'{cores[2]["verde"]}-={cores[2]["limpa"]}' * n

    elif cor == 3:
        mensagem = f'{cores[3]["roxo"]}-={cores[3]["limpa"]}' * n

    elif cor == 5:
        mensagem = f'{cores[5]["vermelho"]}-={cores[5]["limpa"]}' * n

    elif cor == 6:
        mensagem = f'{cores[4]["amarelo"]}-={cores[4]["limpa"]}' * n
    
    elif cor == 7:
        mensagem = f'{cores[5]["vermelho"]}{n}{cores[5]["limpa"]}'
    return print(mensagem)

def atualizacao_txt(info, info2):
    date = datetime.datetime.now()
    texto = f'-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n{info}: {info2}\nDia e hora: {date}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'
    with open('Global-Solution/archives/event.txt', 'a') as file:
        file.write(texto)

def carregarLista():
    with open("Global-Solution/json/cadastro.json", "r") as arquivo:
        return json.load(arquivo)

def salvarCredenciais(email, senha):
    try:
        dados_login = carregarLista("Sprint4/json/clientes.json")
    except FileNotFoundError:
        dados_login = {}

    dados_login[email] = senha

    with open("Sprint4/json/clientes.json", "w") as arquivo:
        json.dump(dados_login, arquivo)

def pwd():
    while True:
        password = getpass.getpass("Senha: ").encode("utf-8")
        confirm_password = getpass.getpass("Confirmar senha: ").encode("utf-8")

        if password == confirm_password and 8 <= len(password) <= 20 and any(char.isdigit() for char in password.decode("utf-8")) and any(char.islower() for char in password.decode("utf-8")) and any(char.isupper() for char in password.decode("utf-8")):
            code = base64.b64encode(password).decode('utf-8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            return hashed, code
        else:
            separador("Senha inválida! Certifique-se de que ela tenha entre 8 e 20 caracteres, contenha pelo menos um número e uma letra maiúscula e minúscula.", 7)

def formatarCpf():

    while True:
        cpf = input("CPF: ")
        while len(cpf) != 11:
            separador('CPF inválido!', 6)
            cpf = input(f'Deve conter 11 caracteres\nDigite seu CPF: ').replace('.', '').replace('-', '').replace(' ', '')

        cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        
        if crud.verifica_cpf_existente(cpf):
            verifica = False
        else:
            verifica = True

        consulta = cellerecpf.consultaCpf(cpf)
        if consulta == True and verifica == True:
            break

    return cpf

def formatarData():
    data  = input("Data de nascimento dd/mm/yyyy: ").strip().replace('/', '')
    while True:
        if len(data) != 8:
            separador('Erro!', 7)
            data = input(' Quantidades de caracteres diferente de 8!\nData de nascimento dd/mm/aaaa: ').replace('/', '').replace(' ', '')
            continue 

        data_atual = datetime.date.today()
        data_nascimento = datetime.date(int(data[4:]), int(data[2:4]), int(data[:2]))
        mes_nascimento = int(data[2:4])
        dia_nascimento = int(data[:2])
        idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (mes_nascimento, dia_nascimento))

        if 18 <= idade <= 100:
            break 

        if idade < 18:
            print(separador('Você é menor de idade!', 6))
        elif idade > 100:
            print(separador('Você tem mais de 100 anos!', 6))

        data = input('Data de nascimento: ')

    return f'{data[:2]}/{data[2:4]}/{data[4:]}'

def formatarCell():
    cell = input("Celular (xx)xxxxx-xxxx: ").replace("(","").replace(")", "").replace("-", "").replace(" ", "")

    while len(cell) != 11:
        separador("Entrada inválida!", 7)
        cell = input("Celular (xx)xxxxx-xxxx: ").replace("(","").replace(")", "").replace("-", "").replace(" ", "")

    return f'({cell[:2]}) {cell[2:7]}-{cell[7:]}'

def formatarTelefone():
    tel = input("Telefone fixo xxxx-xxxx: ").replace("-",'').strip()

    while len(tel) != 8:
        separador("Entrada inválida!", 7)
        tel = input("\nTelefone fixo xxxx-xxxx: ").replace("-",'').strip()

    return f'{tel[:4]}-{tel[4:]}'

def validaEmail():
    status = False
    verifica = False
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+'

    while True:
        email = input("Email: ").lower().strip()
        if re.match(regex, email):
            status = True
        else:
            separador("Email inválido!", 7)
            print("Exemplo: usuario@example.com")
            status = False
            
        if crud.verifica_email_existente(email):
            verifica = False
        else:
            verifica = True
        
        if status == True and verifica == True:
            break

    return email

def logarEmail():
    status = False
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+'

    while status == False:
        email = input("Email: ").lower().strip()
        if re.match(regex, email):
            status = True
        else:
            separador("Email inválido!", 7)
            print("Exemplo: usuario@example.com")

    return email

def centralizar(texto, n):
    largura = n
    texto_formatado = texto.center(largura)

    return print(texto_formatado)

def consultaCep():
    cep = input("Informe seu CEP!\nCaso não saiba apenas tecle ENTER!\nCEP: ").replace(" ", "").replace(".", "").replace("-", "")

    if cep == "":
        link = "https://buscacepinter.correios.com.br/app/endereco/index.php"
        webbrowser.open(link)
        cep = input("CEP: ")
    
    while len(cep) != 8 or not cep.isdigit():
        separador("Inválido!", 7)
        cep = input("Informe seu CEP!\nCaso não saiba apenas tecle ENTER!\nCEP: ").replace(" ", "").replace(".", "").replace("-", "")
    
    cep, dic = viacep.cep(cep)

    return cep, dic

def formata_valor():
    while True:
        try:
            valor = int(input("Valor: R$"))
            valor = round(valor, 2)
            valor_str = '{:,}'.format(int(valor))
            if valor == int(valor):
                valor_str += '.00'
            else:
                valor_str += '.' + '{:02d}'.format(int(valor % 1 * 100))
            return 'R$' + valor_str
        except ValueError:
            separador("Insira um número válido!", 7)

def principal():
    pass

#Programa principal
principal()