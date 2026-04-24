import streamlit as st
import time
from database.cliente import get_client, hash_senha

st.set_page_config(page_title="Nova Senha | MuseIA", layout="centered")
st.title("🔐 Nova Senha MuseIA")

# 1. Tenta capturar o token (seja por link direto ou parâmetro)
token = st.query_params.get("access_token") or st.query_params.get("token")

with st.form("set_password"):
    nova = st.text_input("Nova Senha", type="password")
    confirma = st.text_input("Confirme a Senha", type="password")
    
    if st.form_submit_button("Substituir Senha"):
        if nova == confirma and len(nova) >= 6:
            try:
                supabase = get_client()
                
                # Força o reconhecimento do usuário
                if token:
                    supabase.auth.set_session(token, "")

                # Troca a senha no Auth oficial
                res = supabase.auth.update_user({"password": nova})
                
                # Sincroniza com a tabela 'usuarios'
                # Pegamos o email do resultado da atualização para ser mais seguro
                user_email = res.user.email 
                supabase.table("usuarios").update({"senha": hash_senha(nova)}).eq("email", user_email).execute()
                
                st.success("✅ Senha alterada com sucesso!")
                st.balloons()
                time.sleep(2)
                st.info("Você será redirecionado para o Login em instantes...")
                time.sleep(2)
                st.switch_page("pages/login.py") # Aqui ele volta para onde o cliente entende o sistema
                
            except Exception as e:
                st.error(f"Erro: {e}. O link pode ter expirado. Peça um novo e-mail.")
        else:
            st.warning("Senhas não conferem ou são curtas (mínimo 6 caracteres).")

# No arquivo pages/login.py
st.markdown("---")
if st.button("Escolha seu Agente"):
    # Chamando o arquivo da vitrine diretamente
    st.switch_page("pages/agentes.py")
