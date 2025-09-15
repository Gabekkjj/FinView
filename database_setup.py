import sqlite3

try:
    # Conecta-se ao banco de dados (cria o arquivo se não existir)
    connection = sqlite3.connect('finview.db')
    cursor = connection.cursor()

    # Cria a tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL
    )
    ''')

    # Cria a tabela de lançamentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lancamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        tipo TEXT NOT NULL, -- 'receita' ou 'despesa'
        data TEXT NOT NULL,
        usuario_id INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
    ''')

    # Confirma as alterações
    connection.commit()
    print("Banco de dados e tabelas criados com sucesso.")

except sqlite3.Error as e:
    print(f"Ocorreu um erro ao configurar o banco de dados: {e}")

finally:
    # Fecha a conexão
    if connection:
        connection.close()