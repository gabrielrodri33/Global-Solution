<h1 align="center">🏣 Medi Track</h1>

Esse repositório consiste em uma solução para nossa prova final da faculdade, ele tinha como proposta "Inovação e Tecnologia Moldando o Futuro da Saúde: Prevenção, Automação e Precisão"

<h1 align="center">🚀 Nossa solução</h1>

Nossa solução busca agilizar o acesso a serviços médicos, promovendo a recomendação de hospitais na região. Ao mesmo tempo, otimiza os processos pré-atendimento para proporcionar maior fluidez hospitalar. A funcionalidade de agendamento visa reduzir o risco de esquecimento de consultas por meio de lembretes detalhados, além de simplificar o processo de cancelamento, permitindo que os pacientes o realizem diretamente na plataforma, notificando automaticamente o hospital.

A funcionalidade de pré-triagem tem como propósito capacitar qualquer pessoa a realizar uma análise rápida e inteligente de seus sintomas, indicando o local mais apropriado para obter atendimento médico imediato. Isso proporciona autonomia e segurança ao paciente. Em casos de sintomas mais graves, o direcionamento para o hospital escolhido aumenta as chances de receber pacientes que, de outra forma, poderiam buscar atendimento em outra instituição. Além disso, fornece ferramentas para que o hospital se prepare para atender o paciente prontamente.
Dessa forma, nossa solução facilita o acesso rápido a serviços médicos e amplia a presença digital dos hospitais, contribuindo para atrair mais pacientes.

<h1 align="center">📋 Requisitos do sistema</h1>

- Python 3.x
- Sistema operacional compatível com os comandos 'cls' (Windows) ou 'clear'  
(Linux/Unix)
- Módulo 'webbrowser' para abrir URLs externas no navegador.
- Verifique se os nomes das tabelas já existem no seu banco de dados 

<h1 align="center">🔧 Funcionalidades</h1>

## Lembrete

- Envio automático de lembretes com, pelo menos, um dia de 
antecedência. 
- Detalhes específicos da consulta, como especialidade médica 
(clínico geral, otorrinolaringologista, etc.). 
- Local da consulta com endereço preciso e link de rota. 
- Horário da consulta claramente definido. 
- Alerta para a necessidade de documentos relevantes. 
- Acesso gratuito para pacientes e médicos

## Pré-triagem

### Para o paciente

#### 1 - Avaliação antecipada do paciente: 

- O paciente pode descrever seus sintomas no sistema para ser 
avaliado 
- Sintomas são analisados por IA para identificar possíveis 
diagnósticos e sua gravidade. 
- Cruzamento de dados com amplos datasets de diversas doenças 
e sintomas 

#### 2 - Recomendações personalizadas: 
- Mensagens personalizadas indicando se o paciente deve repousar, 
- procurar atendimento hospitalar ou se há risco imediato de vida. 
- Em casos graves, direcionamento imediato para o hospital mais 
próximo. 

### Para o hospital

#### Processo de triagem agilizado: 
- Notificação antecipada caso um paciente seja direcionado a 
unidade. 
- Pré-ficha do paciente com dados pessoais, sintomas e possíveis 
diagnósticos listados.  
- Chamadas automáticas para casos mais graves, agilizando o 
atendimento de emergência. 

<h1 align="center">⚙️ Execução do projeto</h1>

- Dentro de “crud.py” na função “credenciais”, altere o return para suas credenciais

- Execute o arquivo main.py  

<h1 align="center">💻 Tecnologia</h1>

- Python 3.12.0 
- DDL, DML, DQL

<h1 align="center">📄 Bibliotecas utilizadas</h1>

- mapas: import para criação de mapas dos hospitais parceiros
- time: Biblioteca para pausar o programa e simular os lembretes
- crud: Módulo para interação com o banco de dados.
- bcrypt: Biblioteca para hash e verificação de senhas.
- json: Biblioteca para manipulação de dados JSON.
- base64: Biblioteca para codificação e decodificação base64.
- getpass: Biblioteca para entrada segura de senhas.
- datetime: Módulo para manipulação de datas e horas.
- os: Módulo para interação com o sistema operacional.
- re: Módulo para expressões regulares.
- webbrowser: Módulo para abrir URLs em um navegador da web.
a- api: Módulo contendo APIs externas para consulta de CEP e validação de CPF.
- oracledb: Biblioteca para interação com bancos de dados Oracle.

### Comandos de instalação
- pip install oracledb 
- pip install bcrypt 
- pip install base64 
- pip install webbrowser 

<h1 align="center">📌 Mapas.py</h1>

-  geopy.geocoders.Nominatim: 
Módulo para realizar geocodificação, 
convertendo endereços em coordenadas geográficas (latitude e longitude), 
utilizando o serviço Nominatim. 
- api.viacep: Módulo personalizado que fornece uma função chamada cep para 
obter informações detalhadas com base em um CEP, utilizando a API do 
ViaCEP.
- geopy.exc.GeocoderTimedOut: Exceção utilizada para lidar com situações em 
que o geocodificador excede o tempo limite ao tentar obter coordenadas 
geográficas. 

### Comandos de intalação
- pip install geopy 
