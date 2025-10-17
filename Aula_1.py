faturamento = 1200 # variavel tipo: int -> numero inteiro
custo = 750.0 # variavel tipo: float -> numero com casa decimal

novas_vendas = 100
faturamento = faturamento + novas_vendas

imposto = faturamento * 0.1

lucro = faturamento-custo-imposto

margem_lucro = lucro/faturamento

print("Faturamento foi de", faturamento)
print("O custo foi de", custo)
print("O lucro foi de", lucro)
print("A margem de lucro foi de", round(margem_lucro, 1))

mensagem = "O faturamento da loja foi de tanto" # variavel tipo string -> texto
email = "violantejunior@gmail.com" #variavel tipo string -> texto

teve_lucro = True # variavel tipo boolean

# Mod -> resto da divisão
tempo_contrato = 170
tempo_anos = 170 / 12
print("Tempo em anos", int(tempo_anos))
tempo_meses = 170 % 12
print("Tempo em meses", tempo_meses)
