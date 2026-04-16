import streamlit as st

def verificar_status_pagamento(usuario):
    """Verifica se o usuário tem permissão de uso (Ativo)."""
    if not usuario:
        return False
        
    status = usuario.get("status_pagamento", "pendente")
    ativo = usuario.get("ativo", False)
    bloqueado = usuario.get("bloqueado", False)
    
    # Regra: Status 'ativo', flag 'ativo' True e NÃO bloqueado
    return status == "ativo" and ativo is True and bloqueado is False

def exibir_aviso_bloqueio():
    """Aviso direcionando para o seu link oficial do Mercado Pago/Payhip."""
    st.warning("⚠️ Esta funcionalidade é exclusiva para assinantes ativos.")
    st.info("Seu acesso atual permite apenas a visualização do catálogo.")
    # Seu link de checkout oficial validado:
    link_pagamento = "https://payhip.com/order?link=QFZhd&pricing_plan=ZjBLpyoOBm"
    st.markdown(f"[🚀 **Ativar Assinatura MuseIA Agora**]({link_pagamento})")