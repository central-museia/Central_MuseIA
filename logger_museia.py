import datetime
import os
import streamlit as st

# Nome do arquivo de log
LOG_FILE = "falhas_sistema.txt"

def registrar_falha(origem, erro_objeto):
    """
    Grava os detalhes técnicos em um arquivo de texto.
    """
    try:
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        conteudo_erro = (
            f"--- FALHA DETECTADA EM {timestamp} ---\n"
            f"LOCAL: {origem}\n"
            f"ERRO: {str(erro_objeto)}\n"
            f"{'-' * 40}\n"
        )
        
        # Modo 'a' (append) para adicionar ao final do arquivo
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(conteudo_erro)
            
    except Exception as e:
        # Se falhar o log, mostramos no console do servidor para não travar o usuário
        print(f"Erro crítico ao tentar escrever no log: {str(e)}")

def exibir_painel_debug():
    """Visualização interna para você monitorar a saúde do app."""
    if os.path.exists(LOG_FILE):
        with st.expander("📂 Histórico de Erros Técnicos (Debug)"):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                conteudo = f.read()
                if conteudo:
                    st.code(conteudo, language="text")
                else:
                    st.write("O arquivo de log está vazio.")
            
            if st.button("Limpar Histórico"):
                try:
                    os.remove(LOG_FILE)
                    st.success("Log limpo com sucesso!")
                except:
                    st.error("Não foi possível apagar o arquivo agora.")
    else:
        st.info("Sistema operando normalmente. Nenhuma falha registrada. ✅")
