from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import repository
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_pode_ser_qualquer_coisa'

# --- Rotas de Autenticação ---

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = repository.find_user_by_email(email)
        if user and check_password_hash(user['senha_hash'], senha):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user_exists = repository.find_user_by_email(email)
        if user_exists:
            flash('Este email já está cadastrado.', 'warning')
            return redirect(url_for('register'))
        senha_hash = generate_password_hash(senha)
        repository.create_user(email, senha_hash)
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Rotas do Dashboard e Lançamentos ---

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    lancamentos = repository.get_lancamentos_by_user_id(user_id)
    
    # --- LÓGICA ATUALIZADA PARA O GRÁFICO ---
    lancamentos_sorted = sorted(lancamentos, key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'))
    chart_labels = []
    chart_data = []
    saldo_acumulado = 0
    for l in lancamentos_sorted:
        if l['tipo'] == 'receita':
            saldo_acumulado += l['valor']
        else:
            saldo_acumulado -= l['valor']
        chart_labels.append(l['descricao'])
        chart_data.append(saldo_acumulado)

    total_receitas = sum(l['valor'] for l in lancamentos if l['tipo'] == 'receita')
    total_despesas = sum(l['valor'] for l in lancamentos if l['tipo'] == 'despesa')
    saldo = total_receitas - total_despesas
    
    return render_template('dashboard.html', 
                           lancamentos=lancamentos, 
                           total_receitas=total_receitas,
                           total_despesas=total_despesas,
                           saldo=saldo,
                           chart_labels=chart_labels,
                           chart_data=chart_data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        repository.add_lancamento(
            descricao=request.form['descricao'],
            valor=float(request.form['valor']),
            tipo=request.form['tipo'],
            data_str=request.form['data'],
            usuario_id=session['user_id']
        )
        flash('Lançamento adicionado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_lancamento.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    lancamento = repository.get_lancamento_by_id(id)
    if not lancamento or lancamento['usuario_id'] != session['user_id']:
        flash('Acesso não autorizado ou lançamento não encontrado.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        repository.update_lancamento(
            lancamento_id=id,
            descricao=request.form['descricao'],
            valor=float(request.form['valor']),
            tipo=request.form['tipo'],
            data_str=request.form['data']
        )
        flash('Lançamento atualizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_lancamento.html', lancamento=lancamento)

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    lancamento = repository.get_lancamento_by_id(id)
    if lancamento and lancamento['usuario_id'] == session['user_id']:
        repository.delete_lancamento(id)
        flash('Lançamento deletado com sucesso!', 'success')
    else:
        flash('Acesso não autorizado.', 'danger')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)