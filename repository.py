import sqlite3
from datetime import datetime

DATABASE_URL = 'finview.db'

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

# --- Funções de Usuário ---

def create_user(email, senha_hash):
    """Cria um novo usuário no banco de dados."""
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO usuarios (email, senha_hash) VALUES (?, ?)',
                     (email, senha_hash))
        conn.commit()
    finally:
        conn.close()

def find_user_by_email(email):
    """Busca um usuário pelo email."""
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        return user
    finally:
        conn.close()

# --- Funções de Lançamento (CRUD) ---

def add_lancamento(descricao, valor, tipo, data_str, usuario_id):
    """Adiciona um novo lançamento para um usuário."""
    conn = get_db_connection()
    try:
        # Converte a data para o formato YYYY-MM-DD
        data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
        conn.execute('INSERT INTO lancamentos (descricao, valor, tipo, data, usuario_id) VALUES (?, ?, ?, ?, ?)',
                     (descricao, valor, tipo, data_obj.isoformat(), usuario_id))
        conn.commit()
    finally:
        conn.close()

def get_lancamentos_by_user_id(usuario_id):
    """Busca todos os lançamentos de um usuário, ordenados por data."""
    conn = get_db_connection()
    try:
        lancamentos = conn.execute('SELECT * FROM lancamentos WHERE usuario_id = ? ORDER BY data DESC',
                                   (usuario_id,)).fetchall()
        return lancamentos
    finally:
        conn.close()

def get_lancamento_by_id(lancamento_id):
    """Busca um lançamento específico pelo seu ID."""
    conn = get_db_connection()
    try:
        lancamento = conn.execute('SELECT * FROM lancamentos WHERE id = ?', (lancamento_id,)).fetchone()
        return lancamento
    finally:
        conn.close()

def update_lancamento(lancamento_id, descricao, valor, tipo, data_str):
    """Atualiza um lançamento existente."""
    conn = get_db_connection()
    try:
        data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
        conn.execute('UPDATE lancamentos SET descricao = ?, valor = ?, tipo = ?, data = ? WHERE id = ?',
                     (descricao, valor, tipo, data_obj.isoformat(), lancamento_id))
        conn.commit()
    finally:
        conn.close()

def delete_lancamento(lancamento_id):
    """Deleta um lançamento."""
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM lancamentos WHERE id = ?', (lancamento_id,))
        conn.commit()
    finally:
        conn.close()