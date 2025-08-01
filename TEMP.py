import pyautogui
import time
import os
import tempfile
import shutil

def abrir_executar_e_abrir_temp():
    # Pressiona Windows + R para abrir o Executar
    pyautogui.hotkey('win', 'r')
    time.sleep(1)  # espera a janela abrir

    # Digita 'temp' e pressiona Enter
    pyautogui.write('temp', interval=0.05)
    pyautogui.press('enter')
    time.sleep(2)  # espera a pasta abrir

def selecionar_e_excluir_arquivos():
    # Seleciona todos os arquivos (Ctrl + A)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)

    # Pressiona Delete para excluir
    pyautogui.press('delete')
    time.sleep(1)

    # Tenta confirmar a exclusão (caso apareça janela)
    # Pressiona Enter para confirmar
    pyautogui.press('enter')
    time.sleep(2)  # tempo maior para aguardar possível janela de erro

def tratar_janela_erro_exclusao():
    """
    Trata a janela de erro que aparece quando arquivos não podem ser excluídos
    Seleciona 'Fazer isso para todos' e clica em 'Ignorar'
    """
    print("Tratando possíveis janelas de erro...")
    
    # Aguarda um pouco para a janela de erro aparecer
    time.sleep(1)
    
    # Tenta múltiplas abordagens para lidar com a janela de erro
    for tentativa in range(3):
        try:
            # Método 1: Procura por texto "Fazer isso para todos" e clica
            try:
                # Procura pela checkbox "Fazer isso para todos"
                checkbox_pos = pyautogui.locateOnScreen('fazer_isso_para_todos.png', confidence=0.8)
                if checkbox_pos:
                    pyautogui.click(checkbox_pos)
                    time.sleep(0.5)
            except:
                # Se não encontrar a imagem, tenta método alternativo
                pass
            
            # Método 2: Usa Tab para navegar até a checkbox
            pyautogui.press('tab')
            time.sleep(0.2)
            pyautogui.press('space')  # Marca a checkbox
            time.sleep(0.5)
            
            # Método 3: Procura pelo botão "Ignorar" ou "Skip"
            try:
                ignorar_pos = pyautogui.locateOnScreen('ignorar.png', confidence=0.8)
                if ignorar_pos:
                    pyautogui.click(ignorar_pos)
                    time.sleep(0.5)
                    break
            except:
                pass
            
            # Método 4: Usa Tab para navegar até o botão Ignorar
            pyautogui.press('tab')
            time.sleep(0.2)
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Método 5: Tenta teclas comuns para "Ignorar"
            # Em inglês seria 'S' para Skip, em português pode ser 'I' para Ignorar
            pyautogui.press('i')  # Para "Ignorar"
            time.sleep(0.5)
            
            # Método 6: Se nada funcionar, tenta ESC para fechar
            pyautogui.press('esc')
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Tentativa {tentativa + 1} falhou: {e}")
            time.sleep(1)
            continue
    
    print("Tratamento de janelas de erro concluído.")

def selecionar_e_excluir_arquivos_melhorado():
    """Versão melhorada que trata janelas de erro automaticamente"""
    print("Selecionando todos os arquivos...")
    
    # Seleciona todos os arquivos (Ctrl + A)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)

    print("Iniciando exclusão...")
    # Pressiona Delete para excluir
    pyautogui.press('delete')
    time.sleep(1)

    # Primeira confirmação (se aparecer)
    print("Confirmando exclusão...")
    pyautogui.press('enter')
    time.sleep(2)
    
    # Aguarda e trata possíveis janelas de erro
    print("Aguardando possíveis janelas de erro...")
    time.sleep(3)  # Tempo para janelas de erro aparecerem
    
    # Loop para tratar múltiplas janelas de erro
    for i in range(10):  # Máximo 10 tentativas
        try:
            # Verifica se ainda há janela ativa (título da janela mudou)
            current_window = pyautogui.getActiveWindow()
            if current_window and ("erro" in current_window.title.lower() or 
                                 "error" in current_window.title.lower() or
                                 "excluir" in current_window.title.lower() or
                                 "delete" in current_window.title.lower()):
                
                print(f"Janela de erro detectada (tentativa {i+1}): {current_window.title}")
                
                # Marcar "Fazer isso para todos os itens"
                # Tenta diferentes combinações de Tab para encontrar a checkbox
                for tab_count in range(5):
                    pyautogui.press('tab')
                    time.sleep(0.1)
                
                # Marca a checkbox (geralmente é um Space)
                pyautogui.press('space')
                time.sleep(0.3)
                
                # Navega para o botão "Ignorar" e clica
                # Geralmente Tab algumas vezes até chegar no botão
                for tab_count in range(3):
                    pyautogui.press('tab')
                    time.sleep(0.1)
                
                # Clica no botão (Enter ou Space)
                pyautogui.press('enter')
                time.sleep(1)
                
                # Aguarda a próxima janela
                time.sleep(2)
            else:
                # Não há mais janelas de erro, sai do loop
                break
                
        except Exception as e:
            print(f"Erro ao tratar janela {i+1}: {e}")
            # Se der erro, tenta métodos básicos
            pyautogui.press('i')  # Ignorar
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1)
    
    print("Processo de exclusão via interface concluído.")

def excluir_arquivos_temp_python():
    # Método alternativo para garantir exclusão dos arquivos ignorando erros
    print("Iniciando limpeza via Python...")
    pasta_temp = tempfile.gettempdir()
    arquivos_removidos = 0
    arquivos_ignorados = 0
    
    try:
        itens = os.listdir(pasta_temp)
        total_itens = len(itens)
        print(f"Processando {total_itens} itens...")
        
        for i, item in enumerate(itens):
            caminho = os.path.join(pasta_temp, item)
            try:
                if os.path.isfile(caminho) or os.path.islink(caminho):
                    os.remove(caminho)
                    arquivos_removidos += 1
                elif os.path.isdir(caminho):
                    shutil.rmtree(caminho)
                    arquivos_removidos += 1
                    
                # Mostra progresso a cada 100 itens
                if (i + 1) % 100 == 0:
                    print(f"Processados: {i + 1}/{total_itens}")
                    
            except Exception:
                # Ignora erros (ex: arquivo em uso)
                arquivos_ignorados += 1
                pass
        
        print(f"Arquivos/pastas removidos: {arquivos_removidos}")
        print(f"Arquivos/pastas ignorados: {arquivos_ignorados}")
        
    except Exception as e:
        print(f"Erro ao acessar pasta temp: {e}")

def main():
    print("="*50)
    print("LIMPADOR DE ARQUIVOS TEMPORÁRIOS")
    print("="*50)
    
    print("1. Abrindo Executar e pasta temp...")
    abrir_executar_e_abrir_temp()
    
    print("2. Selecionando e excluindo arquivos via interface...")
    selecionar_e_excluir_arquivos_melhorado()
    
    print("3. Tentando excluir arquivos restantes via Python...")
    excluir_arquivos_temp_python()
    
    print("="*50)
    print("PROCESSO CONCLUÍDO!")
    print("="*50)
    print("- Arquivos foram excluídos via interface gráfica")
    print("- Janelas de erro foram tratadas automaticamente")
    print("- Limpeza adicional foi feita via Python")
    print("- Arquivos em uso foram automaticamente ignorados")

if __name__ == "__main__":
    main()
