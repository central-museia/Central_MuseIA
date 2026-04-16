import streamlit as st
from database.cliente import get_client

def recuperar_senha_ui():
    """Interface para solicitar recuperação de acesso."""
    st.markdown("### 🔑 Recuperar Senha")
    st.write("Insira seu e-mail cadastrado para receber as instruções.")

    email_reset = st.text_input("E-mail de Cadastro").strip().lower()
    
    if st.button("Enviar Link de Recuperação"):
        if email_reset:
            try:
                supabase = get_client()
                # A lógica nativa do Supabase para reset de senha
                response = supabase.auth.reset_password_for_email(email_reset)
                st.success("Se o e-mail estiver cadastrado, você receberá um link em instantes.")
                st.info("Verifique também sua caixa de spam.")
            except Exception as e:
                st.error(f"Erro ao processar solicitação: {str(e)}")
        else:
            st.warning("Por favor, digite seu e-mail.")

    if st.button("Voltar para Login"):
        st.session_state.reset_view = False
        st.rerun()