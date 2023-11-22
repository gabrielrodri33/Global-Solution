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
        sql_query_paciente = """
                            CREATE TABLE paciente (
                                cpf         VARCHAR2(15) NOT NULL,
                                nome        VARCHAR2(100) NOT NULL,
                                email       VARCHAR2(100) NOT NULL,
                                senha       VARCHAR2(1000) NOT NULL,
                                tel_celular VARCHAR2(15),
                                CONSTRAINT paciente_pk PRIMARY KEY (cpf)
                            )"""
        
        sql_query_endereco = """
                            CREATE TABLE endereco (
                                paciente_cpf   VARCHAR2(15) PRIMARY KEY,
                                logradouro    VARCHAR2(255) NOT NULL,
                                bairro        VARCHAR2(255) NOT NULL,
                                numero        VARCHAR2(10),
                                complemento   VARCHAR2(100),
                                cidade        VARCHAR2(100) NOT NULL,
                                estado        VARCHAR2(2) NOT NULL,
                                cep           VARCHAR2(8) NOT NULL,
                                CONSTRAINT endereco_paciente_fk FOREIGN KEY (paciente_cpf) REFERENCES paciente (cpf)
                            )"""
        
        sql_query_bike_modelos = """
                            CREATE TABLE bike_modelos (
                                id_modelo   INTEGER NOT NULL,
                                nome        VARCHAR2(255) NOT NULL,
                                valor_aprox VARCHAR2(35),
                                cor         VARCHAR2(255),
                                num_serie   VARCHAR2(255) NOT NULL,
                                obs             CLOB,
                                cpf_paciente VARCHAR2(15) NOT NULL,
                                CONSTRAINT bike_modelos_pk PRIMARY KEY (id_modelo)
                            )"""

        sql_query_vistoria = """
                            CREATE TABLE vistoria (
                                id_vistoria     INTEGER NOT NULL,
                                dt_inicio       DATE NOT NULL,
                                dt_fim          DATE,
                                aprov           CHAR(1) NOT NULL,
                                bikes_num_serie VARCHAR2(255) NOT NULL,
                                paciente_cpf     VARCHAR2(15) NOT NULL,
                                CONSTRAINT vistoria_pk PRIMARY KEY (id_vistoria),
                                CONSTRAINT vistoria_paciente_fk FOREIGN KEY (paciente_cpf) REFERENCES paciente (cpf)
                            )"""

        cursor.execute(sql_query_paciente)
        cursor.execute(sql_query_endereco)
        cursor.execute(sql_query_bike_modelos)
        cursor.execute(sql_query_vistoria)
        conn.commit()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f'Something went wrong - create: {e}')
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
