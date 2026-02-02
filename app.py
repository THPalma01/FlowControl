from database import criar_banco
from finance import *
from finance import criar_categoria

criar_categoria("Vendas", "Receita")
criar_categoria("Serviços", "Receita")
criar_categoria("Aluguel", "Despesa")
criar_categoria("Fornecedores", "Despesa")

if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado com sucesso!")

print("Faturamento:", faturamento_total())
print("Despesas:", total_despesas())
print("Lucro:", lucro_liquido())
print("Ticket Médio:", ticket_medio())
print("Despesas por categoria:", despesas_por_categoria())
print("Faturamento mensal:", faturamento_mensal())
