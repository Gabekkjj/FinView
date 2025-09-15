# FinView - Dashboard de Controle de Finanças

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Um dashboard de controle de finanças pessoais desenvolvido como projeto para a disciplina de Projeto de Software, aplicando conceitos de arquitetura, SOLID e Design Patterns.

---

##  Funcionalidades Principais

* **Autenticação de Usuário:** Sistema seguro de cadastro e login para garantir a privacidade dos dados.
* **Dashboard Visual:** Painel de controle com um resumo claro de receitas, despesas e saldo atual.
* **Gráfico Dinâmico:** Visualização da evolução do saldo acumulado ao longo do tempo.
* **CRUD de Lançamentos:** Funcionalidade completa para Criar, Ler, Atualizar e Deletar transações financeiras.

---

##  Tecnologias Utilizadas

* **Back-end:** Python 3
* **Framework:** Flask
* **Banco de Dados:** SQLite 3
* **Front-end:** HTML5, CSS3, JavaScript
* **Templates:** Jinja2
* **Visualização de Dados:** Chart.js

---

##  Arquitetura e Conceitos Aplicados

Este projeto foi estruturado para demonstrar a aplicação prática de fundamentos de engenharia de software.

#### **Arquitetura MVC (Model-View-Controller)**
A aplicação segue uma arquitetura MVC adaptada, onde:
* **Model:** A camada de dados é gerenciada pelo `repository.py`, que interage com o banco de dados SQLite.
* **View:** As interfaces são construídas com templates HTML e renderizadas pelo Jinja2.
* **Controller:** As rotas e a lógica de negócio são orquestradas pelo `app.py` usando Flask.

#### **Princípios SOLID**
* **SRP (Princípio da Responsabilidade Única):** A lógica de acesso ao banco de dados foi isolada no `repository.py`, deixando o `app.py` responsável apenas pelo controle das rotas e da lógica de requisição/resposta.
* **DIP (Princípio da Inversão de Dependência):** O padrão Repository abstrai a fonte de dados. A aplicação depende dessa abstração, e não de uma implementação concreta de SQL, facilitando a troca do banco de dados no futuro.

#### **Design Patterns**
* **Repository:** Centraliza toda a lógica de acesso a dados, agindo como uma coleção de objetos de domínio e desacoplando a camada de negócio da camada de persistência.
* **Singleton:** A maneira como o Flask gerencia o contexto da aplicação e a conexão com o banco (através de funções como `get_db_connection`) se assemelha ao padrão Singleton, garantindo um ponto de acesso controlado aos recursos.

---

##  Como Executar o Projeto Localmente

Siga os passos abaixo para rodar o FinView na sua máquina.

### **Pré-requisitos**
* [Python 3.8+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)

### **Instalação**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Gabekkjj/FinView.git](https://github.com/Gabekkjj/FinView.git)
    cd FinView
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Para Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o banco de dados:**
    *Este comando só precisa ser executado uma vez para criar o arquivo `finview.db` e as tabelas.*
    ```bash
    python3 database_setup.py
    ```

5.  **Execute a aplicação:**
    ```bash
    python3 app.py
    ```

6.  Abra seu navegador e acesse `http://127.0.0.1:5000`.
