from database import criar_banco
from finance import (
    criar_categoria,
    faturamento_total,
    total_despesas,
    lucro_liquido,
    ticket_medio,
    despesas_por_categoria,
    faturamento_mensal
)

if __name__ == "__main__":
    # Criar banco primeiro
    criar_banco()
    print("Banco de dados criado com sucesso!")
    
    # Criar categorias padrão
    categorias_padrao = [
        ("Vendas", "Receita"),
        ("Serviços", "Receita"),
        ("Aluguel", "Despesa"),
        ("Fornecedores", "Despesa")
    ]
    
    for nome, tipo in categorias_padrao:
        try:
            criar_categoria(nome, tipo)
        except:
            pass  # Categoria já existe
    
    # Exibir resumo
    print("\n=== Resumo Financeiro ===")
    print(f"Faturamento: R$ {faturamento_total():.2f}")
    print(f"Despesas: R$ {total_despesas():.2f}")
    print(f"Lucro: R$ {lucro_liquido():.2f}")
    print(f"Ticket Médio: R$ {ticket_medio():.2f}")
    print(f"\nDespesas por categoria: {despesas_por_categoria()}")
    print(f"Faturamento mensal: {faturamento_mensal()}")
