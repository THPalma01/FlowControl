from finance import criar_categoria, listar_categorias

# Verificar se já existem categorias antes de criar
categorias_existentes = listar_categorias()
nomes_existentes = [c.nome for c in categorias_existentes]

categorias_padrao = [
    ("Vendas", "Receita"),
    ("Serviços", "Receita"),
    ("Aluguel", "Despesa"),
    ("Fornecedores", "Despesa")
]

for nome, tipo in categorias_padrao:
    if nome not in nomes_existentes:
        criar_categoria(nome, tipo)
        print(f"Categoria '{nome}' criada!")
    else:
        print(f"Categoria '{nome}' já existe.")
