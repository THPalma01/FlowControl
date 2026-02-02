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

## ▶️ Executar

```bash
pip install -r requirements.txt
python init_db.py
python seed.py
python -m streamlit run dashboard.py