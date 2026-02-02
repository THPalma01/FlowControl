# 💼 SmartFinance

Sistema de Gestão Financeira com Dashboard Analítico, Controle de Transações, Relatórios e Autenticação de Usuários.

## 🚀 Funcionalidades
- Cadastro de receitas e despesas
- Dashboard com indicadores financeiros
- Filtro por período
- Comparação entre períodos
- Histórico de transações
- Exportação para Excel
- Geração de relatório em PDF
- Sistema de login

## 🛠 Tecnologias
- Python
- Streamlit
- SQLAlchemy
- SQLite
- Pandas
- Matplotlib
- ReportLab

## ▶️ Como Executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Inicializar banco de dados e criar categorias padrão
```bash
python init_db.py
python seed.py
```

### 3. Executar o dashboard
```bash
streamlit run dashboard.py
```

### 4. (Opcional) Testar funcionalidades via terminal
```bash
python app.py
```

## 📝 Primeiro Acesso
1. Acesse o dashboard no navegador
2. Clique em "Cadastro"
3. Crie sua conta
4. Faça login
5. Comece a registrar suas transações!