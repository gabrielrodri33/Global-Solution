import mapas
import time
import re
import webbrowser
import datetime
import json
import crud
import os
import getpass
import base64
import bcrypt
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api import cellerecpf
from api import viacep
from datetime import datetime, timedelta

# - mapas: import para criação de mapas dos hospitais parceiros
# - time: Biblioteca para pausar o programa e simular os lembretes
# - crud: Módulo para interação com o banco de dados.
# - bcrypt: Biblioteca para hash e verificação de senhas.
# - json: Biblioteca para manipulação de dados JSON.
# - base64: Biblioteca para codificação e decodificação base64.
# - getpass: Biblioteca para entrada segura de senhas.
# - datetime: Módulo para manipulação de datas e horas.
# - os: Módulo para interação com o sistema operacional.
# - re: Módulo para expressões regulares.
# - webbrowser: Módulo para abrir URLs em um navegador da web.
# - api: Módulo contendo APIs externas para consulta de CEP e validação de CPF.
# - oracledb: Biblioteca para interação com bancos de dados Oracle.

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
    date = datetime.now()
    texto = f'-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n{info}: {info2}\nDia e hora: {date}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n'
    with open('Global-Solution/archives/event.txt', 'a') as file:
        file.write(texto)

def carregarLista(mp):
    with open(f"Global-Solution/json/{mp}.json", "r") as arquivo:
        return json.load(arquivo)

def salvarCredenciais(email, senha, mp):
    try:
        with open(f"Global-Solution/json/{mp}.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[email] = senha

    with open(f"Global-Solution/json/{mp}.json", "w") as arquivo:
        json.dump(data, arquivo)

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
            separador('CPF inválido!', 7)
            cpf = input(f'Deve conter 11 caracteres\nDigite seu CPF: ').replace('.', '').replace('-', '').replace(' ', '')

        cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        
        if crud.verifica_cpf_existente(cpf):
            verifica = False
        else:
            verifica = True
            break

        # consulta = cellerecpf.consultaCpf(cpf)
        # if consulta == True and verifica == True:
        #     break

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

def login_user():
    clear_console()
    status = False
    c = 0
    mp = validacao(2)

    if mp == 1:
        mp = 'medicos'
    else:
        mp = 'clientes'

    with open(f"Global-Solution/json/{mp}.json", "r") as file:
        dados_login = json.load(file)
    
    while status == False:
        separador(30, 3)
        centralizar("Login", 60)
        separador(30, 3)
        email = logarEmail()
        senha = getpass.getpass("Senha: ").encode("utf-8")
        senha = base64.b64encode(senha).decode("utf-8")
        
        if email in dados_login and dados_login[email] == senha:
            status = True
            login = True
        else:
            clear_console()
            separador(30, 3)
            separador("Email ou senha incorretos!", 7)
            c += 1
    
        if c == 3:
            clear_console()
            separador(30, 5)
            centralizar("Limite de tentativas atingido!", 60)
            separador(30, 5)
            option = validacao(8)
            if option == 4:
                option = 6
            
            elif option == 2:
                option = 2

            elif option == 3:
                option = 3

            else:
                if mp =='medicos':
                    email = logarEmail()
                    senha, code = pwd()
                    crud.updatePwd("medico", "senha", senha, email)
                else:
                    email = logarEmail()
                    senha, code = pwd()
                    crud.updatePwd("paciente", "senha", senha, email)

                with open(f"Global-Solution/json/{mp}.json", 'r') as arquivo:
                    dados_login = json.load(arquivo)

                dados_login[email] = code

                with open(f"Global-Solution/json/{mp}.json", 'w') as arquivo:
                    json.dump(dados_login, arquivo, indent=2)

                print(f'Valor da chave {email} alterado para {code}.')

                atualizacao_txt("Senha alterada:", email)

                c = 0 

    if status == True:
        clear_console()
        separador(30,1)
        centralizar("Logado!", 60)
        atualizacao_txt("Usuário logado", email)
        if mp == 'medicos':
            print("Sua próxima consulta")
            crm = crud.get_crm_from_email(email)
            data = crud.obter_data_medico(crm)

            if data:
                data_formatada = data[0].strftime('%Y-%m-%d %H:%M:%S')
                contagem_regressiva(data_formatada)
            else:
                print("Nenhuma consulta agendada!")
            
        else:
            option = validacao(7)
            match option:
                case 1:
                    clear_console()
                    separador(30, 1)
                    centralizar("Opções", 60)
                    separador(30, 1)
                    dt_inicio = imprimir_datas()
                    hora_agendamento = imprimir_horarios()
                    hora = hora_agendamento[:2]
                    hora = int(hora) + 1
                    hora_fim = f'{hora}:00:00'

                    dt_inicio = str(dt_inicio)

                    dt_inicio = f"{dt_inicio[:10]} {hora_agendamento}"
                    dt_fim = f"{dt_inicio[:10]} {hora_fim}"

                    desc = input("Descreva o que está sentindo: ")

                    cpf = crud.get_cpf_from_email(email)
                    print(cpf)
                    estado = crud.obter_estado(cpf)
                    id_hospital = crud.obter_id(estado[0])

                    crm = crud.obter_crm()

                    id_tipo = crud.listar_tipos_procedimento()

                    crud.insert_agendamento(dt_inicio, dt_fim, desc, crm, cpf, id_tipo, id_hospital[0])

                case 2:
                    cpf = crud.get_cpf_from_email(email)
                    data = crud.obter_data(cpf)

                    if data:
                        data_formatada = data[0].strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        print("Nenhuma consulta agendada!")
                    contagem_regressiva(data_formatada)
                    cpf = crud.get_cpf_from_email(email)
                    print(cpf)
                    estado = crud.obter_estado(cpf)
                    id_hospital = crud.obter_id(estado[0])
                    hospital = crud.obter_hospital(id_hospital[0])
                    data = {"endereco": hospital[0], "cidade": hospital[1], "estado": hospital[2]}
                    latitude, longitude = mapas.link_hospital(data)
                    url = f"https://www.google.com/maps/place/{latitude},{longitude}"
                    webbrowser.open(url)

    option = validacao(9)
    senha = ""
    return  option, login

def imprimir_horarios():
    c = 1
    print("Horários disponíveis:")
    for hora in range(6, 19):
        hora_agendamento = f"{hora:02d}:00:00"
        print(f"{c}- {hora_agendamento}")
        c += 1

    while True:
        try:
            escolha = int(input("Escolha o número correspondente ao horário desejado: "))
            if 1 <= escolha <= 13:
                return f"{escolha + 5:02d}:00:00"
            else:
                print("Escolha inválida. Por favor, escolha um número entre 1 e 13.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def imprimir_datas():

    hoje = datetime.now()

    proximo_dia = hoje + timedelta(days=1)

    print("Próximos 7 dias:")
    for i in range(7):
        data = proximo_dia + timedelta(days=i)
        print(f"{i + 1}. {data.strftime('%Y-%m-%d')}")

    escolha = int(input("Escolha um dia (1-7): "))

    if 1 <= escolha <= 7:
        data_escolhida = proximo_dia + timedelta(days=escolha - 1)
        print(f"Você escolheu o dia {data_escolhida.strftime('%Y-%m-%d')}")
    else:
        print("Escolha inválida.")

    return data_escolhida

def contagem_regressiva(data_objetivo):
    data_objetivo = datetime.strptime(data_objetivo, "%Y-%m-%d %H:%M:%S")

    while datetime.now() < data_objetivo:
        diferenca = data_objetivo - datetime.now()
        dias_faltando = diferenca.days

        if dias_faltando == 0:
            print(f"A consulta é hoje às {data_objetivo.strftime('%H:%M:%S')}")
            break
        else:
            print(f"Dias faltando: {dias_faltando}")

        time.sleep(10)

        data_objetivo -= timedelta(days=1)

def validacao(dado):
    status = False
    match dado:
        case 1:
            while not status:
                try:
                    clear_console()
                    separador(30, 1)
                    centralizar("Menu principal!", 60)
                    separador(30, 1)
                    option = int(input("1- Fazer login\n2- Fazer cadastro como paciente\n3- Fazer cadastro com médico\n4- Localização de hospitais\n5- Termos de políticas de privacidade\n6- Sair\n"))

                    if 1 <= option <= 6:
                        status = True

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 1 a 6!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")

        case 2:
            while not status:
                try:
                    clear_console()
                    separador(30, 1)
                    centralizar("Tela de login!", 60)
                    separador(30, 1)
                    option = int(input("1- Médico\n2- Paciente\n"))

                    if 1 <= option <= 2:
                        status = True

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 1 a 2!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")

        case 3:
            while not status:
                try:
                    option = int(input("Se todas informações estiverem corretas, digite 0.\nCaso contrário digite a opção que deseja mudar\n"))

                    if 0 <= option <=4:
                        status = True

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 0 a 4!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")
        case 4:
            while not status:
                try:
                    clear_console()
                    option = input("Informações corretas? [S/N]").strip().upper()
                    if option in ["S", "N"]:
                        status = True
                except ValueError as e:
                    print(f"Error: {e}")

        case 5:
            while not status:
                try:
                    option = int(input("Digite o número da especialidade desejada: "))

                    if 1 <= option <= 27:
                        status = True

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 1 a 27!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")
        
        case 6:
            while not status:
                try:
                    option = int(input("Se todas informações estiverem corretas, digite 0.\nCaso contrário digite a opção que deseja mudar\n"))

                    if 0 <= option <=3:
                        status = True

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 0 a 3!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")

        case 7:
            while not status:
                try:
                    option = int(input("1- Agendar consulta\n2- Visualizar consultas agendadas\n"))

                    if 1 <= option <=2:
                        status = True

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 1 a 2!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")

        case 8:
            while not status:
                try:
                    option = int(input("1- Alterar senha\n2- Fazer cadastro como paciente\n3- Fazer cadastro com médico\n4- Sair\n"))

                    if 1 <= option <= 4:
                        status = True

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 1 a 4!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")

        case 9:
            while not status:
                try:
                    clear_console()
                    separador(30, 1)
                    centralizar("Menu principal!", 60)
                    separador(30, 1)
                    option = int(input("1- Localização de hospitais\n2- Termos de políticas de privacidade\n3- Sair\n"))

                    if 1 <= option <= 3:
                        status = True
                        if option == 1:
                            option = 4
                        elif option == 2:
                            option = 5
                        elif option == 3:
                            option = 6

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 1 a 6!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")

        case 10:
            while not status:
                try:
                    option = int(input("1- Todos hospitais\n2- Clínicas\n3- Hospitais HapVida\n4- Imagem e Laboratório\n5- Pronto Atendimento\n6- Outros"))

                    if 1 <= option <= 6:
                        status = True

                    else:
                        clear_console()
                        separador(30, 1)
                        separador("Entrada inválida!", 7)
                        print("Por favor escolha uma opção de 1 a 6!")
                except ValueError:
                    clear_console()
                    separador(30, 1)
                    separador("Entrada inválida!", 7)
                    print("Por favor insira um número")
    return option

def add_dict_endereco(dicionario, logradouro, bairro, localidade, uf, complemento, numero):
    dicionario = {
        'logradouro': logradouro,
        'bairro': bairro,
        'localidade': localidade,
        'uf': uf,
        'complemento': complemento,
        'numero': numero
    }

    print(dicionario)
    return dicionario

def cadastroEndereco(cpf):
    endereco_cliente = {}
    while True:
        separador(30,3)
        centralizar("Endereço", 60)
        separador(30,3)
        cep, endereco = consultaCep()
        logradouro = endereco['logradouro']
        bairro = endereco['bairro']
        localidade = endereco['localidade']
        uf = endereco['uf']

        print(f'Logradouro: {logradouro}')
        print(f'Bairro: {bairro}')
        print(f'Localidade: {localidade}')
        print(f'uf: {uf}')
        correto = validacao(4)
        if correto == "S":
            complemento = input("Complemento (opcional): ")
            numero = input("Número (opcional): ")
            endereco_cliente = add_dict_endereco(endereco_cliente, logradouro, bairro, localidade, uf, complemento, numero)
            break
        atualizacao_txt("Endereço cadastrado", cpf)


    crud.insertEndereco(cpf, logradouro, bairro, numero, complemento, localidade, uf, cep)

    return endereco_cliente

def addDict(dicionario, nome, email, tel_celular, cpf):
    dicionario = { 
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "telefone_celular": tel_celular
    }

    return dicionario

def cadastro_paciente():
    dados_cliente = {}
    clear_console()
    separador(30, 3)
    centralizar("Cadastro", 60)
    separador(30, 3)
    nome = input("Nome: ").strip().title()
    email = validaEmail()
    senha, code = pwd()

    cpf = formatarCpf()
    tel_celular = formatarCell()

    dados_cliente = addDict(dados_cliente, nome, email, tel_celular, cpf)

    atualizacao_txt("Paciente cadastrado", cpf)

    cadastroEndereco(cpf)

    crud.insert_paciente(cpf, nome, senha, email, tel_celular)
    salvarCredenciais(email, code, 'clientes')

    update_paciente(dados_cliente, cpf)

def update_paciente(dados_cliente, cpf):
    mudanca = ""
    while mudanca != 0:
        clear_console()
        separador(30, 2)
        centralizar("Informações de Cadastro", 60)
        separador(30, 2)
        print(f'1- Nome: {dados_cliente["nome"]}\n2- Email: {dados_cliente["email"]}\n3- Celular: {dados_cliente["telefone_celular"]}\n')
        mudanca = validacao(3)

        match mudanca:
            case 1:
                dados_cliente["nome"] = input('Nome: ').strip().title()
                crud.update("paciente", "nome", dados_cliente["nome"], cpf)
                atualizacao_txt("Nome atualizado", dados_cliente["nome"])
            case 2:
                dados_cliente["email"] = validaEmail()
                crud.update("paciente", "email", dados_cliente["email"], cpf)
                atualizacao_txt("Email atualizado", dados_cliente["email"])

            case 3:
                dados_cliente["telefone_celular"] = formatarCell()
                crud.update("paciente", "telefone", dados_cliente["telefone_celular"], cpf)
                atualizacao_txt("Celular atualizado!", dados_cliente["telefone_celular"])

    return dados_cliente["email"]

def especialidade():
    especialidades = [
        "Oncologia Clínica",
        "Ortopedia e Traumatologia",
        "Otorrinolaringologia",
        "Patologia",
        "Patologia Clínica",
        "Patologia Clínica/Medicina Laboratorial",
        "Pediatria",
        "Pneumologia",
        "Pneumologia e Tisiologia",
        "Proctologia",
        "Psiquiatria",
        "Psiquiatria Infantil",
        "Radiodiagnóstico",
        "Radiologia",
        "Radiologia e Diagnóstico por Imagem",
        "Radioterapia",
        "Reumatologia",
        "Sexologia",
        "Terapia Intensiva",
        "Terapia Intensiva Pediátrica",
        "Cuidados Intensivos Pediátricos",
        "Tisiologia",
        "Toco-Ginecologia",
        "Ultrassonografia",
        "Ultrassonografia em Ginecologia e Obstetrícia",
        "Ultrassonografia Geral",
        "Urologia"
    ]
    print("Escolha uma especialidade:")
    for i, especialidade in enumerate(especialidades, start=1):
        print(f"{i}- {especialidade}")

    return especialidades

def obter_especialidade():
    especialidades = especialidade()
    escolha = validacao(5)
    
    if 1 <= escolha <= len(especialidades):
        return escolha
    else:
        print("Opção inválida. Por favor, escolha um número válido.")
        return obter_especialidade(especialidades)

def cadastro_medico():
    dados_medico = {}
    separador(30, 3)
    centralizar("Cadastro médico", 60)
    separador(30, 3)
    crm = input("CRM: ")
    nome = input("Nome: ").strip().title()
    email = validaEmail()
    senha, code = pwd()
    celular = formatarCell()
    clear_console()
    separador(30, 3)
    centralizar("Especialidade!", 60)
    separador(30, 3)
    especialidade = obter_especialidade()

    crud.insert_medico(crm, nome, senha, email, celular, especialidade)
    atualizacao_txt("Médico cadastrado", crm)

    dados_medico = {
        'crm': crm,
        'nome': nome,
        'email': email,
        'celular': celular,
        'especialidade': especialidade
    }

    update_medico(dados_medico)

def update_medico(dados_medico):
    mudanca = ""
    while mudanca != 0:
        # clear_console()
        separador(30, 2)
        centralizar("Informações de Cadastro", 60)
        separador(30, 2)
        especialidade = crud.select_especialidade(dados_medico["especialidade"])
        print(f'1- Nome: {dados_medico["nome"]}\n2- Email: {dados_medico["email"]}\n3- Celular: {dados_medico["celular"]}\n')
        mudanca = validacao(6)
        match mudanca:
            case 1:
                dados_medico["nome"] = input('Nome: ').strip().title()
                crud.update_medico("medico", "nome", dados_medico["nome"], dados_medico["crm"])
                atualizacao_txt("Nome atualizado", dados_medico["nome"])

            case 2:
                dados_medico["email"] = validaEmail()
                crud.update_medico("medico", "email", dados_medico["email"], dados_medico["crm"])
                atualizacao_txt("Email atualizado", dados_medico["email"])

            case 3:
                dados_medico["celular"] = formatarCell()
                crud.update_medico("medico", "telefone", dados_medico["celular"], dados_medico["crm"])
                atualizacao_txt("Número de celular atualizado", dados_medico["celular"])

def menu_principal():
    option = validacao(1)
    clear_console()
    login = False

    while True:
        match option:
            case 1:
                option, login = login_user()

            case 2:
                cadastro_paciente()
                option = 1

            case 3:
                cadastro_medico()

            case 4:
                if login == False:
                    separador(30, 1)
                    print("É necessário estar logado!")
                    print("Carregando tela de login")
                    separador(30, 1)
                    time.sleep(4)
                    option = 1

                else:
                    # option = int(input("1- Todos hospitais\n2- Clínicas\n3- Hospitais HapVida\n4- Imagem e Laboratório\n5- Pronto Atendimento\n6- Outros"))
                    local = validacao(10)
                    mapas.principal('02346-000', '158')
                    if local == 1:
                        url = "C:/FIAP/Computational Thinking Using Python/Global-Solution/Global-Solution/html/todos.html"
                    elif local == 2:
                        url = "C:/FIAP/Computational Thinking Using Python/Global-Solution/Global-Solution/html/clinica.html"
                    elif local == 3:
                        url = "C:/FIAP/Computational Thinking Using Python/Global-Solution/Global-Solution/html/hospitais.html"
                    elif local == 4:
                        url = "C:/FIAP/Computational Thinking Using Python/Global-Solution/Global-Solution/html/imagemlaboratorio.html"
                    elif local == 5:
                        url = "C:/FIAP/Computational Thinking Using Python/Global-Solution/Global-Solution/html/pa.html"
                    elif local == 6:
                        url = "C:/FIAP/Computational Thinking Using Python/Global-Solution/Global-Solution/html/outras.html"
                    webbrowser.open(url)
                    print("Vermelho: Sua localização\nAzul: Clínicas Notredame\nRoxo: Clínicas HapVida\nLaranja: Hospitais\nVermelho escuro: Imagem e Laboratório\nCinza: Pronto Atendimento\nVerde: Outros")

                    option = validacao(1)

            case 5:
                url = "https://www.hapvida.com.br/site/politicas-de-privacidade:~:text=A%20Hapvida%20toma%20providências%20técnicas,não%20é%20acessível%20ao%20público."
                webbrowser.open(url)
                url = "https://www.gndi.com.br/portal-da-privacidade/politica-privacidade"
                webbrowser.open(url)
                option = validacao(1)

            case 7:
                break

def principal():
    crud.create()
    clear_console()
    menu_principal()

#Programa principal
principal()