import streamlit as st
import threading
import os
import tempfile
import shutil
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Limpador de Arquivos Temp",
    page_icon="🧹",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhor aparência
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 4px;
        padding: 12px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 4px;
        padding: 12px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

class TempCleanerApp:
    def __init__(self):
        self.limpando = False
        self.mensagens = []
        self.stats = {
            'removidos': 0,
            'ignorados': 0,
            'total': 0
        }
    
    def adicionar_mensagem(self, msg):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        mensagem_formatada = f"[{timestamp}] {msg}"
        self.mensagens.append(mensagem_formatada)
    
    def obter_tamanho_pasta(self):
        """Calcula o tamanho total da pasta temp"""
        pasta_temp = tempfile.gettempdir()
        tamanho_total = 0
        
        try:
            for dirpath, dirnames, filenames in os.walk(pasta_temp):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        tamanho_total += os.path.getsize(fp)
                    except:
                        pass
        except:
            pass
        
        return tamanho_total
    
    def formatar_bytes(self, bytes_size):
        """Converte bytes para formato legível"""
        for unidade in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unidade}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"
    
    def limpar_arquivos(self):
        """Executa a limpeza dos arquivos"""
        self.adicionar_mensagem("=" * 60)
        self.adicionar_mensagem("INICIANDO LIMPEZA DE ARQUIVOS TEMPORÁRIOS")
        self.adicionar_mensagem("=" * 60)
        
        pasta_temp = tempfile.gettempdir()
        removidos = 0
        ignorados = 0
        
        try:
            itens = os.listdir(pasta_temp)
            self.stats['total'] = len(itens)
            self.adicionar_mensagem(f"Total de itens encontrados: {len(itens)}")
            self.adicionar_mensagem("Iniciando remoção...")
            
            for i, item in enumerate(itens):
                caminho = os.path.join(pasta_temp, item)
                
                try:
                    # Remove arquivo ou link simbólico
                    if os.path.isfile(caminho) or os.path.islink(caminho):
                        os.remove(caminho)
                        removidos += 1
                        
                    # Remove diretório
                    elif os.path.isdir(caminho):
                        try:
                            shutil.rmtree(caminho, ignore_errors=True)
                            removidos += 1
                        except Exception:
                            ignorados += 1
                    
                    # Log de progresso a cada 50 itens
                    if (i + 1) % 50 == 0:
                        self.adicionar_mensagem(
                            f"Progresso: {i + 1}/{len(itens)} "
                            f"(Removidos: {removidos}, Ignorados: {ignorados})"
                        )
                    
                except PermissionError:
                    ignorados += 1
                    
                except Exception as e:
                    ignorados += 1
            
            self.stats['removidos'] = removidos
            self.stats['ignorados'] = ignorados
            
            self.adicionar_mensagem("=" * 60)
            self.adicionar_mensagem(f"✓ LIMPEZA CONCLUÍDA!")
            self.adicionar_mensagem(f"  Removidos: {removidos}")
            self.adicionar_mensagem(f"  Ignorados: {ignorados}")
            self.adicionar_mensagem(f"  Taxa de sucesso: {(removidos/(removidos+ignorados)*100):.1f}%")
            self.adicionar_mensagem("=" * 60)
            
        except Exception as e:
            self.adicionar_mensagem(f"✗ Erro durante limpeza: {e}")
        
        self.limpando = False

# Inicializa session state
if 'app' not in st.session_state:
    st.session_state.app = TempCleanerApp()

app = st.session_state.app

# Cabeçalho
st.markdown("# 🧹 Limpador de Arquivos Temporários")
st.markdown("---")

# Coluna para informações
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Informações")
    pasta_temp = tempfile.gettempdir()
    st.text(f"Pasta: {pasta_temp}")
    
    tamanho = app.obter_tamanho_pasta()
    st.text(f"Tamanho: {app.formatar_bytes(tamanho)}")

with col2:
    st.markdown("### ✅ Estatísticas")
    if app.stats['total'] > 0:
        st.metric("Removidos", app.stats['removidos'])
        st.metric("Ignorados", app.stats['ignorados'])
    else:
        st.info("Nenhuma limpeza executada ainda")

st.markdown("---")

# Botão principal de limpeza
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🚀 INICIAR LIMPEZA", key="btn_limpar", use_container_width=True):
        app.limpando = True
        app.mensagens = []
        app.stats = {'removidos': 0, 'ignorados': 0, 'total': 0}
        
        # Executa em thread separada para não bloquear a UI
        thread = threading.Thread(target=app.limpar_arquivos)
        thread.daemon = True
        thread.start()
        thread.join()  # Aguarda conclusão

st.markdown("---")

# Área de log
st.markdown("### 📋 Log de Operações")

# Container para o log com auto-scroll
log_container = st.container()

if app.mensagens:
    with log_container:
        for msg in app.mensagens:
            if "ERRO" in msg or "✗" in msg:
                st.error(msg)
            elif "SUCESSO" in msg or "✓" in msg or "CONCLUÍDA" in msg:
                st.success(msg)
            elif "=" * 10 in msg or "INICIANDO" in msg or "Progresso" in msg:
                st.info(msg)
            else:
                st.text(msg)
else:
    st.text("Nenhuma operação executada. Clique no botão acima para começar.")

# Sidebar com informações adicionais
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    st.markdown("#### Informações sobre o Limpador")
    st.markdown("""
    Este aplicativo remove automaticamente:
    - Arquivos temporários de aplicações
    - Cache do Windows
    - Arquivos em diretórios temporários
    - Diretórios vazios
    
    **Nota:** Arquivos em uso serão automaticamente ignorados.
    """)
    
    st.markdown("---")
    st.markdown("#### 💡 Dicas")
    st.markdown("""
    1. Feche aplicações abertas para liberar arquivos em uso
    2. Execute com permissões de administrador para melhor eficiência
    3. Faça backup importante antes de começar
    4. A operação pode levar alguns minutos
    """)
    
    st.markdown("---")
    st.markdown("#### 📝 Versão")
    st.text("v1.0 - Limpador Automático de Temp")