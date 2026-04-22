# utils/session.py
import streamlit as st

def reset_agente_session():
    keys = [
        "processamento_liberado",
        "resultado_gerado",
        "executar_agora",
        "input_execucao",
        "resultado_final",
        "agente_selecionado"
    ]

    for k in keys:
        st.session_state[k] = False if k in [
            "processamento_liberado",
            "resultado_gerado",
            "executar_agora"
        ] else None
