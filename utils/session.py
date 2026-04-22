
def reset_agente_session():
    import streamlit as st
    
    keys = [
        "processamento_liberado",
        "resultado_gerado",
        "executar_agora",
        "input_execucao",
        "resultado_final",
        "agente_selecionado"
    ]
    
    for k in keys:
        st.session_state[k] = False if "liberado" in k or "gerado" in k or "executar" in k else None
