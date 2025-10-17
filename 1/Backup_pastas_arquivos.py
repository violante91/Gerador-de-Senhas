import os
from tkinter.filedialog import askdirectory
import shutil
import datetime

# Seleciona a pasta do computador
nome_pasta_selecionada = askdirectory()

# Lista os arquivos e pastas da pasta selecionada, excluindo a pasta de backup
lista_arquivos = [f for f in os.listdir(nome_pasta_selecionada) if f != 'backup']

# Define o caminho da pasta de backup
nome_pasta_backup = 'backup'
nome_completo_pasta_backup = os.path.join(nome_pasta_selecionada, nome_pasta_backup)

# Cria a pasta de backup caso não exista
if not os.path.exists(nome_completo_pasta_backup):
    os.mkdir(nome_completo_pasta_backup)

# Define a pasta de backup atual com data e hora
data_atual = datetime.datetime.today().strftime('%Y-%m-%d %H.%M.%S')
pasta_backup_atual = os.path.join(nome_completo_pasta_backup, data_atual)

# Cria a pasta de backup da data atual
if not os.path.exists(pasta_backup_atual):
    os.mkdir(pasta_backup_atual)

# Copia arquivos e pastas para a pasta de backup
for item in lista_arquivos:
    print(item)
    caminho_item = os.path.join(nome_pasta_selecionada, item)
    destino_item = os.path.join(pasta_backup_atual, item)

    if os.path.isfile(caminho_item):
        shutil.copy2(caminho_item, destino_item)
    elif os.path.isdir(caminho_item):
        shutil.copytree(caminho_item, destino_item)