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
                cep           VARCHAR2(8) NOT NULL,
                PRIMARY KEY (paciente_cpf)
            )
        """

        sql_query_hospital = """
            CREATE TABLE hospital (
                id_hospital     INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
                nome            VARCHAR2(50) NOT NULL,
                endereco_numero NUMBER(6,0) NOT NULL,
                paciente_cpf    VARCHAR2(15) NOT NULL,
                PRIMARY KEY (id_hospital),
                FOREIGN KEY (paciente_cpf) REFERENCES endereco (paciente_cpf)
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

        sql_query_agendamento = """
            CREATE TABLE agendamento (
                id_agendamento    INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
                dt_agendamento    DATE,
                dt_fim            DATE,
                descricao         VARCHAR2(255) NOT NULL,
                crm               VARCHAR2(25) NOT NULL,
                cpf               VARCHAR2(11) NOT NULL,
                tipo              VARCHAR2(50) NOT NULL,
                id_hospital       INTEGER NOT NULL,
                PRIMARY KEY (id_agendamento),
                FOREIGN KEY (crm) REFERENCES medico (crm),
                FOREIGN KEY (cpf) REFERENCES paciente (cpf),
                FOREIGN KEY (id_hospital) REFERENCES hospital (id_hospital)
            )
        """

        cursor.execute(sql_query_endereco)
        cursor.execute(sql_query_hospital)
        cursor.execute(sql_query_especialidade)
        cursor.execute(sql_query_medico)
        cursor.execute(sql_query_paciente)
        cursor.execute(sql_query_agendamento)

        conn.commit()
        print("Tabelas criadas com sucesso!")
        insert_especialidades()
    except Exception as e:
        print(f'Something went wrong - create: {e}')
    finally:
        cursor.close()
        conn.close()

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
            print(f"O CPF associado ao email {email} é: {cpf}")
            return cpf
        else:
            print(f"Nenhum registro encontrado para o email {email}")
            return None

    except Exception as e:
        print(f"Algo deu errado - get_cpf_from_email: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

def select_id():
    try:
        conn, cursor = conexao()

        sql_query = "SELECT MAX(id_modelo) FROM bike_modelos"
        cursor.execute(sql_query)
        max_id = cursor.fetchone()[0]

        if max_id is not None:
            return max_id + 1
        else:
            return 1

    except Exception as e:
        print(f"Algo deu errado - select_id: {e}")
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
