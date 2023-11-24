import oracledb
import datetime

def credenciais():
    return "RM98626", "311003"

def conexao():
    try:
        user, pwd = credenciais()
        conn = oracledb.connect(user=user, password=pwd, host="oracle.fiap.com.br", port="1521", service_name="orcl")
        cursor = conn.cursor()
        # print(f"Conexão {conn.version}")
    except Exception as e:
        print(f'Something went wrong - conexao: {e}')
    return conn, cursor

def create():
    try:
        conn, cursor = conexao()

        sql_query_endereco = """
            CREATE TABLE endereco (
                paciente_cpf  VARCHAR2(15),
                logradouro    VARCHAR2(255) NOT NULL,
                bairro        VARCHAR2(255) NOT NULL,
                numero        VARCHAR2(10),
                complemento   VARCHAR2(100),
                cidade        VARCHAR2(100) NOT NULL,
                estado        VARCHAR2(2) NOT NULL,
                cep           VARCHAR2(9) NOT NULL,
                PRIMARY KEY (paciente_cpf)
            )
        """

        sql_query_hospital = """
            CREATE TABLE hospital (
                id_hospital     INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
                nome            VARCHAR2(255)  NOT NULL,
                cep             VARCHAR2(15)  NOT NULL,
                logradouro      VARCHAR2(255) NOT NULL,
                bairro          VARCHAR2(255) NOT NULL,
                estado          VARCHAR2(2)   NOT NULL,
                PRIMARY KEY (id_hospital)
            )
        """

        sql_query_especialidade = """
            CREATE TABLE especialidade(
                id_especialidade NUMBER(6, 0) NOT NULL,
                especialidade    VARCHAR2(60) NOT NULL,
                PRIMARY KEY (id_especialidade)
            )
        """

        sql_query_medico = """
            CREATE TABLE medico (
                crm              VARCHAR2(25) NOT NULL,
                nome             VARCHAR2(50) NOT NULL,
                senha            VARCHAR2(1000) NOT NULL,
                email            VARCHAR2(50) NOT NULL,
                telefone         VARCHAR2(15) NOT NULL,
                id_especialidade NUMBER(6,0) NOT NULL,
                PRIMARY KEY (crm),
                FOREIGN KEY (id_especialidade) REFERENCES especialidade (id_especialidade)
            )
        """

        sql_query_paciente = """
            CREATE TABLE paciente (
                cpf             VARCHAR2(15) NOT NULL,
                nome            VARCHAR2(50) NOT NULL,
                senha           VARCHAR2(1000) NOT NULL,
                email           VARCHAR2(50) NOT NULL,
                telefone        VARCHAR2(15) NOT NULL,
                PRIMARY KEY (cpf)
            )
        """

        sql_query_tipo = """
            CREATE TABLE tipo_procedimento (
                id_tipo NUMBER(6, 0) NOT NULL,
                tipo VARCHAR2(50) NOT NULL,
                PRIMARY KEY (id_tipo) 
            )
        """

        sql_query_agendamento = """
            CREATE TABLE agendamento (
                id_agendamento    INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
                dt_agendamento    TIMESTAMP,
                dt_fim            TIMESTAMP,  
                descricao         VARCHAR2(255) NOT NULL,
                crm               VARCHAR2(25) NOT NULL,
                cpf               VARCHAR2(14) NOT NULL,
                id_tipo           NUMBER(6, 0) NOT NULL,
                id_hospital       INTEGER NOT NULL,
                PRIMARY KEY (id_agendamento),
                FOREIGN KEY (crm) REFERENCES medico (crm),
                FOREIGN KEY (cpf) REFERENCES paciente (cpf),
                FOREIGN KEY (id_hospital) REFERENCES hospital (id_hospital),
                FOREIGN KEY (id_tipo) REFERENCES tipo_procedimento (id_tipo)
            )
        """

        cursor.execute(sql_query_endereco)
        cursor.execute(sql_query_hospital)
        cursor.execute(sql_query_especialidade)
        cursor.execute(sql_query_medico)
        cursor.execute(sql_query_paciente)
        cursor.execute(sql_query_tipo)
        cursor.execute(sql_query_agendamento)

        conn.commit()
        print("Tabelas criadas com sucesso!")

        insert_especialidades()
        insert_hospitais()
        inserts_procedimento()

        senha_amanda = b'$2b$12$YYYhmKr5j6OwzWHOAe88H.hlkZAHTymdsshxzYhcqWDg5v4RwH6ai'
        senha_paulo = b'$2b$12$XLOFES2/MDVLGno4csXYheCp.03B7jJgHr9mNE9rTdpPWXvCytK9m'
        insert_medico('945162', 'Paulo Godoy', senha_paulo, 'pagodoy@gmail.com', '(11)91234-5678', '5')
        insertEndereco('123.456.789-11', 'Rua Chile', 'Vila Rosália', ' ', ' ', 'Guarulhos', 'SP', '07064-050')
        insert_paciente('123.456.789-11', 'Amanda Moreira', senha_amanda, 'amanda@gmail.com', '(11)98765-4321')
        insert_agendamento(
            dt_agendamento='2023-11-23 7:00:00',
            dt_fim='2023-11-23 08:00:00',
            descricao='Consulta médica',
            crm='945162',
            cpf='123.456.789-11',
            id_tipo=3,
            id_hospital=17
        )

    except Exception as e:
        print(f'Something went wrong - create: {e}')
    finally:
        # cursor.close()
        conn.close()

def insert_tipo_procedimento(id_tipo, tipo):
    conn = None
    cursor = None
    try:
        conn, cursor = conexao()

        # Insert into tipo_procedimento table
        sql_query = """
            INSERT INTO tipo_procedimento (id_tipo, tipo)
            VALUES (:id_tipo, :tipo)
        """
        
        cursor.execute(sql_query, {
            'id_tipo': id_tipo,
            'tipo': tipo
        })

        conn.commit()
        print("Cadastro de tipo de procedimento realizado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro - insert_tipo_procedimento: {e}")
    finally:
        cursor.close()
        conn.close()

def inserts_procedimento():
    insert_tipo_procedimento(1, 'Exame de Sangue')
    insert_tipo_procedimento(2, 'Ultrassonografia')
    insert_tipo_procedimento(3, 'Colonoscopia')
    insert_tipo_procedimento(4, 'Cirurgia Cardíaca')
    insert_tipo_procedimento(5, 'Consulta Médica')
    insert_tipo_procedimento(6, 'Limpeza de Pele')
    insert_tipo_procedimento(7, 'Fisioterapia')
    insert_tipo_procedimento(8, 'Radioterapia')
    insert_tipo_procedimento(9, 'Parto Normal')
    insert_tipo_procedimento(10, 'Tomografia Computadorizada')

def insert_agendamento(dt_agendamento, dt_fim, descricao, crm, cpf, id_tipo, id_hospital):
    try:
        conn, cursor = conexao()

        sql_query = """
            INSERT INTO agendamento (dt_agendamento, dt_fim, descricao, crm, cpf, id_tipo, id_hospital)
            VALUES (TO_TIMESTAMP(:dt_agendamento, 'YYYY-MM-DD HH24:MI:SS'), 
                    TO_TIMESTAMP(:dt_fim, 'YYYY-MM-DD HH24:MI:SS'), 
                    :descricao, :crm, :cpf, :id_tipo, :id_hospital)
        """
        
        cursor.execute(sql_query, {
            'dt_agendamento': dt_agendamento,
            'dt_fim': dt_fim,
            'descricao': descricao,
            'crm': crm,
            'cpf': cpf,
            'id_tipo': id_tipo,
            'id_hospital': id_hospital
        })

        conn.commit()
        print("Agendamento realizado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro - insert_agendamento: {e}")
    finally:
        cursor.close()
        conn.close()


def insert_hospital(nome, cep, logradouro, bairro, estado):
    try:
        conn, cursor = conexao()

        sql_query = """
            INSERT INTO hospital (nome, cep, logradouro, bairro, estado)
            VALUES (:nome, :cep, :logradouro, :bairro, :estado)
        """
        
        cursor.execute(sql_query, {
            'nome': nome,
            'cep': cep,
            'logradouro': logradouro,
            'bairro': bairro,
            'estado': estado
        })

        conn.commit()
        print("Cadastro de hospital realizado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro - insert_hospital: {e}")
    finally:
        cursor.close()
        conn.close()

def insert_hospitais():
    insert_hospital('Hospital e Maternidade Maceió', '57000-001', 'Avenida Presidente Getúlio Vargas', 'Serraria', 'AL')
    insert_hospital('Hospital e Maternidade Rio Amazonas', '69079-210', 'Rua Belém', 'São Francisco', 'AM')
    insert_hospital('Hospital e Maternidade Cetro', '48005-240', 'Rua Elvira Dórea', 'Centro', 'BA')
    insert_hospital('Hospital e Maternidade Antonio Prudente', '60055-401', 'Avenida Aguanambi, 1827', 'Bairro de Fátima', 'CE')
    insert_hospital('Hospital e Maternidade Brasiliense', '70390-135', 'SEPS 713 / 913 - Asa Sul', 'Brasília', 'DF')
    insert_hospital('Hospital e Maternidade América', '74175-150', 'Alameda Coronel Joaquim Bastos, nº 120', 'Setor Marista', 'GO')
    insert_hospital('Hospital e Maternidade Guarás', '65030-130', 'Rua Armando Vieira da Silva', 'São Luís', 'MA')
    insert_hospital('Hospital e Maternidade Imesa', '37130-000', 'Rua Adolfo Engel, 19', 'Jardim Tropical', 'MG')
    insert_hospital('Hospital e Maternidade da Paraíba', '58040-040', 'Av. Júlia Freire, 1058', 'Expedicionários', 'PB')
    insert_hospital('Hospital do Cabo', '54505-560', 'Av. Presidente Vargas, 428', 'Centro', 'PE')
    insert_hospital('Hospital e Maternidade Rio Poty', '64002-300', 'Rua Lucídio Freitas, 2070', 'Marquês de Paranaguá', 'PI')
    insert_hospital('Hospital e Maternidade Santa Brígida', '80620-000', 'Rua Guilherme Pugsley, 1705', 'Água Verde', 'PR')
    insert_hospital('Hospital e Maternidade Intermédica Jacarepaguá', '22745-005', 'Estrada dos Três Rios, 542', 'Jacarepaguá', 'RJ')
    insert_hospital('Hospital e Maternidade Celina Guimarães', '59611-320', 'Rua Raimundo Leão de Moura, 10', 'Nova Betânia', 'RN')
    insert_hospital('Hospital e Maternidade Geral Joinville', '89204-100', 'Rua Itaiópolis, 128', 'Bairro América', 'SC')
    insert_hospital('Hospital e Maternidade Gabriel Soares', '49015-110', 'Rua Itabaiana, 690', 'Centro', 'SE')
    insert_hospital('Hospital e Maternidade Imesa', '14801-150', 'Av José Bonifácio, 569', 'Centro', 'SP')

def insert_especialidades():
    try:
        conn, cursor = conexao()

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

        sql_query = "INSERT INTO especialidade (id_especialidade, especialidade) VALUES (:id_especialidade, :especialidade)"

        for i, especialidade in enumerate(especialidades, start=1):
            cursor.execute(sql_query, {
                'id_especialidade': i,
                'especialidade': especialidade
            })

        conn.commit()
        print("Inserção de especialidades realizada com sucesso!")
    except Exception as e:
        print(f'Ocorreu um erro - insert_especialidades: {e}')
    finally:
        cursor.close()
        conn.close()

def insert_paciente(cpf, nome, senha, email, telefone):
    try:
        conn, cursor = conexao()

        sql_query = """
            INSERT INTO paciente (cpf, nome, senha, email, telefone)
            VALUES (:cpf, :nome, :senha, :email, :telefone)
        """
        
        cursor.execute(sql_query, {
            'cpf': cpf,
            'nome': nome,
            'senha': senha,
            'email': email,
            'telefone': telefone
        })

        conn.commit()
        print("Cadastro realizado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro - insert_paciente: {e}")
    finally:
        cursor.close()
        conn.close()

def insert_medico(crm, nome, senha, email, telefone, id_especialidade):
    try:
        conn, cursor = conexao()

        sql_query = """
            INSERT INTO medico (crm, nome, senha, email, telefone, id_especialidade)
            VALUES (:crm, :nome, :senha, :email, :telefone, :id_especialidade)
        """
        
        cursor.execute(sql_query, {
            'crm': crm,
            'nome': nome,
            'senha': senha,
            'email': email,
            'telefone': telefone,
            'id_especialidade': id_especialidade
        })

        conn.commit()
        print("Cadastro de médico realizado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro - insert_medico: {e}")
    finally:
        cursor.close()
        conn.close()


def verifica_email_existente(email):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT COUNT(*) FROM paciente WHERE email = :email"
        cursor.execute(sql_query, email=email)

        resultado = cursor.fetchone()
        count = resultado[0]

        if count > 0:
            print(f'E-mail: "{email}" já cadastrado.')
            return True
        else:
            return False

    except Exception as e:
        print(f'Something went wrong - verifica_email_existente: {e}')
    finally:
        cursor.close()
        conn.close()

def verifica_cpf_existente(cpf):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT COUNT(*) FROM paciente WHERE cpf = :cpf"
        cursor.execute(sql_query, cpf=cpf)

        resultado = cursor.fetchone()
        count = resultado[0]

        if count > 0:
            print(f"CPF {cpf} já cadastrado.")
            return True
        else:
            return False

    except Exception as e:
        print(f'Something went wrong - verifica_cpf_existente: {e}')
    finally:
        cursor.close()
        conn.close()

def update(table, dado, value, cpf):
    try:
        conn, cursor = conexao()

        if isinstance(value, (int, float)):
            value_str = str(value)
        else:
            value_str = f"'{value.replace("'", "''")}'"

        sql_query = f"UPDATE {table} SET {dado} = {value_str} WHERE cpf = :cpf"
        cursor.execute(sql_query, {'cpf': cpf})
        conn.commit()
        print("Atualizado com sucesso")
    except Exception as e:
        print(f'Something went wrong - update: {e}')
    finally:
        cursor.close()
        conn.close()

def update_medico(table, dado, value, crm):
    try:
        conn, cursor = conexao()

        if isinstance(value, (int, float)):
            value_str = str(value)
        else:
            value_str = f"'{value.replace("'", "''")}'"

        sql_query = f"UPDATE {table} SET {dado} = {value_str} WHERE crm = :crm"
        cursor.execute(sql_query, {'crm': crm})
        conn.commit()
        print("Atualizado com sucesso")
    except Exception as e:
        print(f'Something went wrong - update: {e}')
    finally:
        cursor.close()
        conn.close()

def select_especialidade(id_especialidade):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT especialidade FROM especialidade WHERE id_especialidade = :id_especialidade"
        cursor.execute(sql_query, id_especialidade=id_especialidade)

        resultados = cursor.fetchall()

        if resultados:
            return resultados[0][0]
        else:
            return None

    except Exception as e:
        print(f'Something went wrong - select_especialidade: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def select(dado1, tbl, dado2):
    try:
        conn, cursor = conexao()

        sql_query = f"SELECT {dado1} FROM {tbl} WHERE {dado2} = :dado2"
        cursor.execute(sql_query, dado2=dado2)

        resultados = cursor.fetchall()

        for resultado in resultados:
            print(f"{dado1}: {resultado[0]}")

    except Exception as e:
        print(f'Something went wrong - select: {e}')
    finally:
        cursor.close()
        conn.close()

def updatePwd(table, dado, value_bytes, email):
    try:
        conn, cursor = conexao()

        value_hex = value_bytes.hex()
        value_str = f"HEXTORAW('{value_hex}')"

        sql_query = f"UPDATE {table} SET {dado} = {value_str} WHERE email = :email"
        cursor.execute(sql_query, {'email': email})
        conn.commit()
        print("Atualizado com sucesso")
    except Exception as e:
        print(f'Something went wrong - updatePwd: {e}')
    finally:
        cursor.close()
        conn.close()

def insertEndereco(cpf, logradouro, bairro, numero, complemento, cidade, estado, cep):
    try:
        conn, cursor = conexao()

        sql_query = "INSERT INTO endereco (paciente_cpf, logradouro, bairro, numero, complemento, cidade, estado, cep) VALUES (:paciente_cpf, :logradouro, :bairro, :numero, :complemento, :cidade, :estado, :cep)"
        cursor.execute(sql_query, {
            'paciente_cpf': cpf,
            'logradouro': logradouro,
            'bairro': bairro,
            'numero': numero,
            'complemento': complemento,
            'cidade': cidade,
            'estado': estado,
            'cep': cep
        })
        conn.commit()
        print("Cadastro realizado com sucesso!")
    except Exception as e:
        print(f"Something went wrong - insert {e}")
    finally:
        cursor.close()
        conn.close()

def get_cpf_from_email(email):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT cpf FROM paciente WHERE email = :email"
        cursor.execute(sql_query, {'email': email})

        result = cursor.fetchone()

        if result:
            cpf = result[0]
            # print(f"O CPF associado ao email {email} é: {cpf}")
            return cpf
        else:
            # print(f"Nenhum registro encontrado para o email {email}")
            return None

    except Exception as e:
        print(f"Algo deu errado - get_cpf_from_email: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

def get_crm_from_email(email):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT crm FROM medico WHERE email = :email"
        cursor.execute(sql_query, {'email': email})

        result = cursor.fetchone()

        if result:
            crm = result[0]
            # print(f"O CPF associado ao email {email} é: {cpf}")
            return crm
        else:
            # print(f"Nenhum registro encontrado para o email {email}")
            return None

    except Exception as e:
        print(f"Algo deu errado - get_cpf_from_email: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

def obter_estado(cpf):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT estado FROM endereco WHERE paciente_cpf = :cpf"
        cursor.execute(sql_query, {'cpf': cpf})

        estado = cursor.fetchone()

        return estado

    except Exception as e:
        print(f"Ocorreu um erro - obter_estado_por_cpf: {e}")
    finally:
        cursor.close()
        conn.close()

def obter_crm():
    try:
        conn, cursor = conexao()

        sql_query = """
            SELECT crm
            FROM medico
            ORDER BY DBMS_RANDOM.VALUE
            FETCH FIRST 1 ROW ONLY
        """

        cursor.execute(sql_query)
        resultado = cursor.fetchone()

        if resultado:
            crm_aleatorio = resultado[0]
            # print(f"CRM: {crm_aleatorio}")
            return crm_aleatorio
        else:
            print("Não há médicos cadastrados.")
            return None

    except Exception as e:
        print(f"Ocorreu um erro - obter_crm_aleatorio: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def obter_id(estado):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT id_hospital FROM hospital WHERE estado = :estado"
        cursor.execute(sql_query, {'estado': estado})

        estado = cursor.fetchone()

        return estado

    except Exception as e:
        print(f"Ocorreu um erro - obter_id: {e}")
    finally:
        cursor.close()
        conn.close()

def obter_data(cpf):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT dt_agendamento FROM agendamento WHERE cpf = :cpf"
        cursor.execute(sql_query, {'cpf': cpf})

        data = cursor.fetchone()

        return data

    except Exception as e:
        print(f"Ocorreu um erro - obter_data: {e}")
    finally:
        cursor.close()
        conn.close()

def obter_data_medico(crm):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT dt_agendamento FROM agendamento WHERE crm = :crm"
        cursor.execute(sql_query, {'crm': crm})

        data = cursor.fetchone()

        return data

    except Exception as e:
        print(f"Ocorreu um erro - obter_data: {e}")
    finally:
        cursor.close()
        conn.close()

def obter_hospital(id_hospital):
    try:
        conn, cursor = conexao()

        sql_query = "SELECT logradouro, bairro, estado FROM hospital WHERE id_hospital = :id_hospital"
        cursor.execute(sql_query, {'id_hospital': id_hospital})

        info_hospital = cursor.fetchone()

        return info_hospital

    except Exception as e:
        print(f"Ocorreu um erro - obter_info_hospital: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_tipos_procedimento():
    try:
        conn, cursor = conexao()

        while True:
            sql_query = """
                SELECT id_tipo, tipo
                FROM tipo_procedimento
                ORDER BY id_tipo
            """

            cursor.execute(sql_query)
            resultados = cursor.fetchall()

            if resultados:
                for i, (id_tipo, tipo) in enumerate(resultados, start=1):
                    print(f"{i}- {tipo}")

                escolha = input("Digite o número da opção desejada: ")

                try:
                    escolha = int(escolha)
                    if 1 <= escolha <= len(resultados):
                        id_tipo_escolhido, tipo_escolhido = resultados[escolha - 1]
                        return id_tipo_escolhido
                    else:
                        print("Opção inválida. Tente novamente.")
                except ValueError:
                    print("Por favor, digite um número válido.")
            else:
                print("Não há tipos de procedimento cadastrados.")
                return None

    except Exception as e:
        print(f"Ocorreu um erro - listar_tipos_procedimento: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def insert(cpf, nome, dt_nasc, tel_fixo, tel_celular, email, senha):
    try:
        conn, cursor = conexao()

        dt_nasc_formatada = datetime.strptime(dt_nasc, '%d/%m/%Y').strftime('%Y-%m-%d')

        sql_query = "INSERT INTO paciente (cpf, nome, dt_nasc, tel_fixo, tel_celular, email, senha) VALUES (:cpf, :nome, TO_DATE(:dt_nasc, 'YYYY-MM-DD'), :tel_fixo, :tel_celular, :email, :senha)"
        cursor.execute(sql_query, {
            'cpf': cpf,
            'nome': nome,
            'dt_nasc': dt_nasc_formatada,
            'tel_fixo': tel_fixo,
            'tel_celular': tel_celular,
            'email': email,
            'senha': senha
        })
        conn.commit()
        print("Cadastro realizado com sucesso!")
    except Exception as e:
        print(f"Something went wrong - insert {e}")
    finally:
        cursor.close()
        conn.close()

create()