import pyautogui
import time
import os
import tempfile
import shutil
import stat
from pathlib import Path

def abrir_executar_e_abrir_temp():
    """Abre a pasta temp usando Windows + R"""
    print("Abrindo pasta de arquivos temporários...")
    # Pressiona Windows + R para abrir o Executar
    pyautogui.hotkey('win', 'r')
    time.sleep(1)  # espera a janela abrir

    # Digita '%temp%' e pressiona Enter
    pyautogui.write('%temp%', interval=0.05)
    pyautogui.press('enter')
    time.sleep(2)  # espera a pasta abrir

def selecionar_e_excluir_arquivos():
    """Tenta excluir arquivos via interface gráfica"""
    print("Selecionando arquivos via interface...")
    
    # Seleciona todos os arquivos (Ctrl + A)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)

    # Pressiona Delete para excluir
    pyautogui.press('delete')
    time.sleep(1)

    # Tenta confirmar a exclusão se aparecer janela de confirmação
    try:
        pyautogui.press('enter')
        time.sleep(1)
        
        # Se aparecer janela de erro ou permissão, pressiona "Pular" ou "Ignorar"
        # Tentativa de pressionar Tab + Enter para pular arquivos protegidos
        pyautogui.press('tab')
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(1)
    except:
        pass

def remover_protecao_arquivo(caminho):
    """Remove proteção de escrita de um arquivo"""
    try:
        # Remove atributo de somente leitura
        os.chmod(caminho, stat.S_IWRITE)
        return True
    except:
        return False

def excluir_arquivos_temp_python():
    """Método Python para excluir arquivos temporários com tratamento robusto de erros"""
    pasta_temp = tempfile.gettempdir()
    arquivos_excluidos = 0
    arquivos_ignorados = 0
    pastas_excluidas = 0
    pastas_ignoradas = 0
    
    print(f"Limpando pasta: {pasta_temp}")
    
    try:
        itens = list(os.listdir(pasta_temp))
        total_itens = len(itens)
        print(f"Total de itens encontrados: {total_itens}")
        
        for i, item in enumerate(itens, 1):
            caminho = os.path.join(pasta_temp, item)
            
            # Mostra progresso a cada 50 itens
            if i % 50 == 0 or i == total_itens:
                print(f"Processando item {i}/{total_itens}...")
            
            try:
                if os.path.isfile(caminho) or os.path.islink(caminho):
                    # Tenta remover proteção antes de excluir
                    if os.path.exists(caminho):
                        remover_protecao_arquivo(caminho)
                        os.remove(caminho)
                        arquivos_excluidos += 1
                        
                elif os.path.isdir(caminho):
                    # Tenta excluir diretório recursivamente
                    def handle_remove_readonly(func, path, exc):
                        """Handler para remover proteção de arquivos somente leitura"""
                        if os.path.exists(path):
                            os.chmod(path, stat.S_IWRITE)
                            func(path)
                    
                    shutil.rmtree(caminho, onerror=handle_remove_readonly)
                    pastas_excluidas += 1
                    
            except PermissionError:
                # Arquivo em uso ou sem permissão
                if os.path.isfile(caminho):
                    arquivos_ignorados += 1
                else:
                    pastas_ignoradas += 1
                continue
                
            except FileNotFoundError:
                # Arquivo já foi excluído
                continue
                
            except OSError as e:
                # Outros erros do sistema (nome muito longo, caracteres inválidos, etc.)
                if os.path.isfile(caminho):
                    arquivos_ignorados += 1
                else:
                    pastas_ignoradas += 1
                continue
                
            except Exception:
                # Qualquer outro erro
                if os.path.isfile(caminho):
                    arquivos_ignorados += 1
                else:
                    pastas_ignoradas += 1
                continue
                
    except Exception as e:
        print(f"Erro ao acessar pasta temporária: {e}")
        return
    
    # Relatório final
    print("\n" + "="*50)
    print("RELATÓRIO DE LIMPEZA")
    print("="*50)
    print(f"Arquivos excluídos: {arquivos_excluidos}")
    print(f"Arquivos ignorados: {arquivos_ignorados}")
    print(f"Pastas excluídas: {pastas_excluidas}")
    print(f"Pastas ignoradas: {pastas_ignoradas}")
    print(f"Total processado: {arquivos_excluidos + arquivos_ignorados + pastas_excluidas + pastas_ignoradas}")

def limpar_outras_pastas_temp():
    """Limpa outras pastas temporárias comuns do Windows"""
    pastas_adicionais = [
        os.path.expandvars(r'%USERPROFILE%\AppData\Local\Temp'),
        os.path.expandvars(r'%WINDIR%\Temp'),
        os.path.expandvars(r'%USERPROFILE%\Recent'),
    ]
    
    for pasta in pastas_adicionais:
        if os.path.exists(pasta) and pasta != tempfile.gettempdir():
            print(f"\nLimpando pasta adicional: {pasta}")
            try:
                for item in os.listdir(pasta):
                    caminho = os.path.join(pasta, item)
                    try:
                        if os.path.isfile(caminho):
                            remover_protecao_arquivo(caminho)
                            os.remove(caminho)
                        elif os.path.isdir(caminho):
                            shutil.rmtree(caminho, ignore_errors=True)
                    except:
                        continue  # Ignora erros silenciosamente
            except:
                print(f"Não foi possível acessar: {pasta}")

def main():
    print("="*60)
    print("LIMPADOR DE ARQUIVOS TEMPORÁRIOS")
    print("="*60)
    
    resposta = input("Deseja usar interface gráfica também? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\n1. Abrindo interface gráfica...")
        abrir_executar_e_abrir_temp()
        
        print("2. Tentando excluir via interface...")
        selecionar_e_excluir_arquivos()
        
        # Pausa para o usuário fechar a janela se necessário
        input("\nPressione Enter após fechar a janela do Explorer para continuar...")
    
    print("\n3. Executando limpeza via Python...")
    excluir_arquivos_temp_python()
    
    resposta_extra = input("\nDeseja limpar pastas temporárias adicionais? (s/n): ").lower().strip()
    if resposta_extra in ['s', 'sim', 'y', 'yes']:
        print("\n4. Limpando pastas adicionais...")
        limpar_outras_pastas_temp()
    
    print("\n" + "="*50)
    print("PROCESSO CONCLUÍDO!")
    print("="*50)
    print("Todos os arquivos possíveis foram excluídos.")
    print("Arquivos em uso ou protegidos foram automaticamente ignorados.")
    
    input("\nPressione Enter para finalizar...")

if __name__ == "__main__":
    main()