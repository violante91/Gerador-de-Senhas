# inputs
#email = input("Escreva seu e-mail: ")
#nome = input("Seu primeiro nome: ")

#print(nome, email)

#print(f"{nome}, verifique seu email: {email} que enviamos um link de confirmação")

# Listas
Vendas = [100, 50, 14, 20, 30, 700]

# Soma dos elementos
total_vendas = sum(Vendas)
print(total_vendas)
#tamanho da lista
quantidade_vendas = len(Vendas)
print(total_vendas)

# max e min
print(max(Vendas))
print(min(Vendas))

#pegar posição
print(Vendas[0])

Lista_produtos = ["iphone", "airpod", "ipad", "macbook"]

#produto_procurado = input("Pesquise pelo nome do produto: ")
#produto_procurado = produto_procurado.lower()

#print(produto_procurado in Lista_produtos)

# Adicionar um item
Lista_produtos.append("apple watch")
print(Lista_produtos)

# Remover um item
Lista_produtos.remove("apple watch")
print(Lista_produtos)

Lista_produtos.pop(0)
print(Lista_produtos)
# Editar um item
precos = [1000, 1500, 3500]
precos[0] = precos[0] *1.5
print(precos)

# Contar quantas vezes um item aparece na lista
Lista_produtos = ["iphone", "airpod", "ipad", "macbook", "iphone", "iphone", "ipad"]
print(Lista_produtos.count("ipad"))

# Ordenar uma Lista
Vendas.sort()
print(Vendas)