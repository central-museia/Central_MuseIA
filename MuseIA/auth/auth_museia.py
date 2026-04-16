import streamlit as st
from database.cliente import validar_login

def exibir_saudacao():
    """Exibe o nome do usuário no topo da página se ele estiver logado."""
    if st.session_state.get("logado") and st.session_state.get("usuario"):
        nome = st.session_state.usuario.get('nome', '').split()[0] # Pega só o primeiro nome
        st.markdown(f"### Bem-vinda de volta, **{nome}**! ✨")
    else:
        st.markdown("### Bem-vinda à **MuseIA Digital**")

def inicializar_sessao():
    """Define o estado inicial. Se não houver usuário, é um 'Visitante'."""
    if "logado" not in st.session_state:
        st.session_state.logado = False
    if "usuario" not in st.session_state:
        st.session_state.usuario = None

def login_ui():
    """Interface de login lateral ou central, sem travar o app."""
    with st.sidebar:
        if not st.session_state.logado:
            st.markdown("### 🔐 Área do Assinante")
            email = st.text_input("E-mail").strip().lower()
            senha = st.text_input("Senha", type="password")
            
            if st.button("Entrar na MuseIA"):
                usuario = validar_login(email, senha)
                if usuario:
                    st.session_state.logado = True
                    st.session_state.usuario = usuario
                    st.success(f"Olá, {usuario['nome']}!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha inválidos.")
        else:
            st.write(f"👤 {st.session_state.usuario['nome']}")
            if st.button("Sair"):
                st.session_state.clear()
                st.rerun()

def pode_utilizar():
    """
    Função global para ser usada antes de rodar qualquer Agente.
    Exemplo: if pode_utilizar(): rodar_agente()
    """
    from core.pagamentos import verificar_status_pagamento, exibir_aviso_bloqueio
    
    if not st.session_state.logado:
        st.error("Você precisa estar logado para usar os agentes.")
        return False
        
    if verificar_status_pagamento(st.session_state.usuario):
        return True
    else:
        exibir_aviso_bloqueio()
        return False