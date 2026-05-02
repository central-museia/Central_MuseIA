import streamlit as st
from utils.ia import executar_ia, montar_prompt
from utils.scraping import extrair_texto_resumido

# ... (motores web, texto, decisao e estruturado permanecem iguais) ...

# =========================================
# 🔥 ORQUESTRADOR PRINCIPAL ATUALIZADO
# =========================================
def executar_agente(texto, regras, codigo_python=None):
    # Recupera o objeto completo do agente que está na memória do Streamlit
    agente_completo = st.session_state.get("agente_selecionado", {})
    
    if not regras and not codigo_python:
        return texto

    # 🔹 PRIORIDADE 1: CÓDIGO PYTHON (CHASSI DINÂMICO)
    if codigo_python:
        try:
            # Preparamos o dicionário de configuração para o Chassi
            # Ele agora envia o nome do robô e as regras do banco
            config_envio = {
                "nome": agente_completo.get("nome", "Agente MuseIA"),
                "regras_processamento": agente_completo.get("regras_processamento", {}),
                "prompt": agente_completo.get("prompt_texto", "") # O prompt que buscaremos
            }

            escopo = {}
            exec(codigo_python, escopo)

            if "executar" in escopo:
                # Passamos o texto e o dicionário de config para o Chassi
                return escopo["executar"](texto, config_envio)

            return "⚠️ Função 'executar' não encontrada no código."

        except Exception as e:
            return f"⚠️ Erro ao executar código do agente: {str(e)}"

    # 🔹 PRIORIDADE 2: MOTOR PADRÃO (Legado)
    # ... (restante do código original do motor_nome e usar_ia) ...
