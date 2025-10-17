import pyautogui
import time
import os
import tempfile
import shutil
import threading
from collections import defaultdict

class TempCleaner:
    def __init__(self, callback=None):
        self.callback = callback
        self.stats = {
            'removidos': 0,
            'ignorados': 0,
            'total': 0,
            'mensagens': []
        }
    
    def log(self, mensagem):
        """Registra mensagem e envia para callback se existir"""
        print(mensagem)
        self.stats['mensagens'].append(mensagem)
        if self.callback:
            self.callback(mensagem)
    
    def abrir_executar_e_abrir_temp(self):
        """Abre a pasta temporária via Executar"""
        self.log("Abrindo Executar e pasta temporária...")
        try:
            pyautogui.hotkey('win', 'r')
            time.sleep(1)
            pyautogui.write('temp', interval=0.05)
            pyautogui.press('enter')
            time.sleep(3)
            self.log("Pasta temporária aberta com sucesso")
        except Exception as e:
            self.log(f"Erro ao abrir pasta: {e}")
    
    def tratar_janela_erro(self):
        """Trata janelas de erro com foco em marcar 'Fazer isso para todos'"""
        self.log("Tratando possíveis janelas de erro...")
        
        try:
            time.sleep(1)
            
            # Tenta Tab para encontrar e marcar a checkbox "Fazer isso para todos"
            for tentativa in range(3):
                try:
                    # Navega até a checkbox (geralmente a primeira opção focável)
                    pyautogui.press('tab')
                    time.sleep(0.2)
                    
                    # Marca a checkbox com Space
                    pyautogui.press('space')
                    self.log(f"Checkbox marcada (tentativa {tentativa + 1})")
                    time.sleep(0.5)
                    break
                except Exception as e:
                    self.log(f"Tentativa {tentativa + 1} falhou: {e}")
                    time.sleep(0.5)
            
            # Navega para o botão "Ignorar" e clica
            for _ in range(4):
                pyautogui.press('tab')
                time.sleep(0.1)
            
            pyautogui.press('enter')
            time.sleep(1)
            self.log("Botão Ignorar acionado")
            
        except Exception as e:
            self.log(f"Erro ao tratar janela: {e}")
    
    def selecionar_e_excluir_interface(self):
        """Seleciona e exclui arquivos via interface gráfica"""
        self.log("Iniciando exclusão via interface...")
        
        try:
            # Seleciona todos os arquivos
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            self.log("Todos os arquivos selecionados")
            
            # Pressiona Delete
            pyautogui.press('delete')
            time.sleep(1)
            
            # Confirmação inicial
            pyautogui.press('enter')
            time.sleep(2)
            
            # Aguarda e trata múltiplas janelas de erro
            self.log("Aguardando possíveis janelas de erro...")
            time.sleep(3)
            
            for i in range(15):  # Máximo 15 janelas de erro
                try:
                    # Verifica se ainda há janela ativa
                    current_window = pyautogui.getActiveWindow()
                    
                    if (current_window and 
                        any(keyword in current_window.title.lower() 
                            for keyword in ['erro', 'error', 'excluir', 'delete', 'confirm'])):
                        
                        self.log(f"Janela de erro detectada: {current_window.title}")
                        self.tratar_janela_erro()
                        time.sleep(2)
                    else:
                        break
                        
                except Exception as e:
                    self.log(f"Erro na iteração {i + 1}: {e}")
                    # Tenta método alternativo
                    pyautogui.press('i')  # Ignorar
                    time.sleep(0.5)
                    pyautogui.press('enter')
                    time.sleep(1)
            
            self.log("Exclusão via interface concluída")
            
        except Exception as e:
            self.log(f"Erro durante exclusão: {e}")
    
    def excluir_arquivos_python(self):
        """Exclui arquivos restantes via Python com tratamento robusto de erros"""
        self.log("\nIniciando limpeza via Python...")
        
        pasta_temp = tempfile.gettempdir()
        arquivos_removidos = 0
        arquivos_ignorados = 0
        
        try:
            # Primeira passagem: arquivos
            self.log(f"Pasta temporária: {pasta_temp}")
            itens = os.listdir(pasta_temp)
            self.stats['total'] = len(itens)
            self.log(f"Total de itens a processar: {len(itens)}")
            
            for i, item in enumerate(itens):
                caminho = os.path.join(pasta_temp, item)
                
                try:
                    # Tenta remover arquivo ou link simbólico
                    if os.path.isfile(caminho) or os.path.islink(caminho):
                        os.remove(caminho)
                        arquivos_removidos += 1
                        
                    # Tenta remover diretório
                    elif os.path.isdir(caminho):
                        try:
                            shutil.rmtree(caminho, ignore_errors=True)
                            arquivos_removidos += 1
                        except Exception:
                            arquivos_ignorados += 1
                    
                    # Mostra progresso
                    if (i + 1) % 50 == 0:
                        progresso = f"Processados: {i + 1}/{len(itens)}"
                        self.log(progresso)
                        
                except PermissionError:
                    # Arquivo em uso ou sem permissão - ignora silenciosamente
                    arquivos_ignorados += 1
                    
                except Exception:
                    # Qualquer outro erro - ignora silenciosamente
                    arquivos_ignorados += 1
            
            self.stats['removidos'] = arquivos_removidos
            self.stats['ignorados'] = arquivos_ignorados
            
            self.log(f"\n✓ Arquivos/pastas removidos: {arquivos_removidos}")
            self.log(f"⊘ Arquivos/pastas ignorados (em uso): {arquivos_ignorados}")
            
        except Exception as e:
            self.log(f"Erro ao acessar pasta temp: {e}")
    
    def executar_completo(self):
        """Executa o processo completo de limpeza"""
        self.log("=" * 60)
        self.log("LIMPADOR DE ARQUIVOS TEMPORÁRIOS - VERSÃO REFINADA")
        self.log("=" * 60)
        
        try:
            # Método 1: Interface gráfica
            self.log("\n[ETAPA 1] Tentando limpeza via interface...")
            self.abrir_executar_e_abrir_temp()
            self.selecionar_e_excluir_interface()
            
        except Exception as e:
            self.log(f"Aviso: Erro na limpeza via interface: {e}")
        
        try:
            # Método 2: Limpeza via Python (sempre executado)
            self.log("\n[ETAPA 2] Executando limpeza complementar via Python...")
            self.excluir_arquivos_python()
            
        except Exception as e:
            self.log(f"Erro durante limpeza Python: {e}")
        
        self.log("\n" + "=" * 60)
        self.log("PROCESSO CONCLUÍDO COM SUCESSO!")
        self.log("=" * 60)
        
        return self.stats

def executar_limpeza(callback=None):
    """Função wrapper para usar em APIs"""
    cleaner = TempCleaner(callback=callback)
    return cleaner.executar_completo()

if __name__ == "__main__":
    # Execução direta
    stats = executar_limpeza()
    print("\n" + "=" * 60)
    print("RESUMO FINAL:")
    print(f"Removidos: {stats['removidos']}")
    print(f"Ignorados: {stats['ignorados']}")
    print("=" * 60)