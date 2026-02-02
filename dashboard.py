import streamlit as st

# st.set_page_config DEVE ser a primeira chamada Streamlit
st.set_page_config(page_title="SmartFinance Dashboard", layout="wide")

import pandas as pd
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from finance import (
    adicionar_transacao,
    despesas_periodo,
    despesas_por_categoria_periodo,
    faturamento_mensal_periodo,
    faturamento_periodo,
    faturamento_total,
    listar_categorias,
    listar_transacoes_periodo,
    total_despesas,
    lucro_liquido,
    ticket_medio,
    despesas_por_categoria,
    faturamento_mensal,
    criar_usuario,
    autenticar_usuario,
    resumo_periodo
)

# Função movida para antes de seu uso
def variacao_percentual(atual, anterior):
    if anterior == 0:
        return 0
    return ((atual - anterior) / anterior) * 100

if "logado" not in st.session_state:
    st.session_state.logado = False
    
if not st.session_state.logado:
    st.title("🔐 SmartFinance Login")

    aba = st.radio("Escolha", ["Login", "Cadastro"])

    if aba == "Cadastro":
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Criar Conta"):
            if not nome or not email or not senha:
                st.error("Todos os campos são obrigatórios!")
            elif len(senha) < 6:
                st.warning("A senha deve ter pelo menos 6 caracteres.")
            else:
                try:
                    criar_usuario(nome, email, senha)
                    st.success("Usuário criado! Faça login.")
                except Exception as e:
                    st.error("Erro ao criar usuário. O email pode já estar cadastrado.")

    if aba == "Login":
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar"):
            if not email or not senha:
                st.error("Preencha email e senha!")
            else:
                user = autenticar_usuario(email, senha)
                if user:
                    st.session_state.logado = True
                    st.session_state.usuario = user.nome
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")

    st.stop()

st.sidebar.success(f"Logado como: {st.session_state.usuario}")

if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()

st.title("💼 SmartFinance — Painel Financeiro Inteligente")

st.subheader("📅 Filtro de Período")

col_data1, col_data2 = st.columns(2)

with col_data1:
    data_inicio = st.date_input("Data Inicial")

with col_data2:
    data_fim = st.date_input("Data Final")

st.divider()
st.subheader("📊 Comparação Entre Períodos")

colA1, colA2 = st.columns(2)
colB1, colB2 = st.columns(2)

with colA1:
    inicio1 = st.date_input("Período 1 - Início", key="p1i")
with colA2:
    fim1 = st.date_input("Período 1 - Fim", key="p1f")

with colB1:
    inicio2 = st.date_input("Período 2 - Início", key="p2i")
with colB2:
    fim2 = st.date_input("Período 2 - Fim", key="p2f")

r1, d1, l1 = resumo_periodo(inicio1, fim1)
r2, d2, l2 = resumo_periodo(inicio2, fim2)

# ================= INDICADORES PRINCIPAIS =================

col1, col2, col3, col4 = st.columns(4)

receitas = faturamento_periodo(data_inicio, data_fim)
despesas = despesas_periodo(data_inicio, data_fim)
lucro = receitas - despesas
ticket = receitas  # pode melhorar depois

col1.metric("💰 Faturamento", f"R$ {receitas:.2f}")
col2.metric("📉 Despesas", f"R$ {despesas:.2f}")
col3.metric("📊 Lucro Líquido", f"R$ {lucro:.2f}")
col4.metric("🧾 Receita no período", f"R$ {ticket:.2f}")

st.divider()

st.divider()
st.subheader("+ Registrar Nova Transação")

with st.form("form_transacao"):
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    data = st.date_input("Data")

    categorias = listar_categorias()
    cat_dict = {f"{c.nome} ({c.tipo})": c.id for c in categorias}

    categoria_nome = st.selectbox("Categoria", list(cat_dict.keys()))

    submitted = st.form_submit_button("Salvar")

    if submitted:
        adicionar_transacao(
            descricao,
            valor,
            data,
            cat_dict[categoria_nome]
        )
        st.success("Transação registrada com sucesso!")
        st.rerun()

st.markdown("### 🔎 Resultado da Comparação")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Faturamento",
    f"P1: R$ {r1:.2f} | P2: R$ {r2:.2f}",
    f"{variacao_percentual(r2, r1):.1f}%"
)

col2.metric(
    "Despesas",
    f"P1: R$ {d1:.2f} | P2: R$ {d2:.2f}",
    f"{variacao_percentual(d2, d1):.1f}%"
)

col3.metric(
    "Lucro",
    f"P1: R$ {l1:.2f} | P2: R$ {l2:.2f}",
    f"{variacao_percentual(l2, l1):.1f}%"
)

# ================= GRÁFICO 1 — DESPESAS POR CATEGORIA =================

st.subheader("📉 Para onde o dinheiro está indo")

dados_despesas = despesas_por_categoria_periodo(data_inicio, data_fim)

if dados_despesas:
    categorias = [d[0] for d in dados_despesas]
    valores = [d[1] for d in dados_despesas]

    fig1, ax1 = plt.subplots()
    ax1.pie(valores, labels=categorias, autopct='%1.1f%%')
    ax1.set_title("Despesas por Categoria")

    st.pyplot(fig1)
else:
    st.info("Sem dados de despesas ainda.")

# ================= GRÁFICO 2 — FATURAMENTO MENSAL =================

st.subheader("📈 Evolução do Faturamento Mensal")

dados_mensais = faturamento_mensal_periodo(data_inicio, data_fim)

if dados_mensais:
    df = pd.DataFrame(dados_mensais, columns=["Mes", "Valor"])
    df = df.sort_values("Mes")

    fig2, ax2 = plt.subplots()
    ax2.plot(df["Mes"], df["Valor"], marker="o")
    ax2.set_xlabel("Mês")
    ax2.set_ylabel("Faturamento")
    ax2.set_title("Faturamento ao Longo do Tempo")

    st.pyplot(fig2)
else:
    st.info("Sem dados de faturamento ainda.")


st.divider()
st.subheader("📜 Histórico de Transações")

dados_tabela = listar_transacoes_periodo(data_inicio, data_fim)

if dados_tabela:
    df_tabela = pd.DataFrame(dados_tabela, columns=[
        "Descrição", "Valor", "Data", "Categoria", "Tipo"
    ])

    st.dataframe(df_tabela, use_container_width=True)
else:
    st.info("Nenhuma transação encontrada para o período selecionado.")


st.subheader("📤 Exportar Dados")

if dados_tabela:
    df_export = pd.DataFrame(dados_tabela, columns=[
        "Descrição", "Valor", "Data", "Categoria", "Tipo"
    ])

    buffer = io.BytesIO()
    df_export.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    st.download_button(
        label="⬇️ Baixar Histórico em Excel",
        data=buffer,
        file_name="historico_financeiro.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def gerar_relatorio_pdf(dados, receitas, despesas, lucro):
    caminho = "relatorio_financeiro.pdf"
    c = canvas.Canvas(caminho, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica", 12)
    c.drawString(50, altura - 50, "Relatório Financeiro - SmartFinance")

    c.drawString(50, altura - 80, f"Faturamento: R$ {receitas:.2f}")
    c.drawString(50, altura - 100, f"Despesas: R$ {despesas:.2f}")
    c.drawString(50, altura - 120, f"Lucro Líquido: R$ {lucro:.2f}")

    y = altura - 160
    c.drawString(50, y, "Histórico de Transações:")
    y -= 20

    for d in dados:
        linha = f"{d[2]} | {d[0]} | R$ {d[1]:.2f} | {d[3]} ({d[4]})"
        c.drawString(50, y, linha)
        y -= 18
        if y < 50:
            c.showPage()
            y = altura - 50

    c.save()
    return caminho

if dados_tabela:
    if st.button("📄 Gerar Relatório em PDF"):
        caminho_pdf = gerar_relatorio_pdf(dados_tabela, receitas, despesas, lucro)
        with open(caminho_pdf, "rb") as f:
            st.download_button(
                "⬇️ Baixar Relatório PDF",
                f,
                file_name="relatorio_financeiro.pdf",
                mime="application/pdf"
            )