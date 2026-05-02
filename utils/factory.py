import streamlit as st  # 👈 ADICIONE ESTA LINHA AQUI
from utils.ia import executar_ia, montar_prompt
from utils.scraping import extrair_texto_resumido

# ... restante do código (motor_web, motor_texto, etc) ...

def executar_agente(texto, regras, codigo_python=None):
    # Agora o st.session_state será reconhecido corretamente
    agente_completo = st.session_state.get("agente_selecionado", {})
    
    if not regras and not codigo_python:
        return texto

    if codigo_python:
        try:
            config_envio = {
                "id": agente_completo.get("id"),
                "nome": agente_completo.get("nome"),
                "regras_processamento": agente_completo.get("regras_processamento", {}),
                "prompt": agente_completo.get("prompt_texto", "")
            }

            escopo = {}
            exec(codigo_python, escopo)

            if "executar" in escopo:
                return escopo["executar"](texto, config_envio)

            return "⚠️ Função 'executar' não encontrada."
        except Exception as e:
            return f"⚠️ Erro: {str(e)}"
    
    # ... restante do orquestrador ...
