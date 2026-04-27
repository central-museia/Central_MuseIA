import streamlit as st
from supabase import create_client  # Mantenha o nome original da biblioteca aqui

def get_supabase_contato():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    # O motor é o mesmo, mas a conexão agora é exclusiva para o contato
    return create_client(url, key)

def inserir_mensagem_contato(nome, email, assunto, mensagem):
    try:
        # Aqui chamamos a sua nova função de conexão
        supabase_contato = get_supabase_contato()
        
        dados = {
            "nome": nome,
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem,
            "status": "Pendente"
        }
        
        supabase_contato.table("fale_conosco").insert(dados).execute()
        return True
        
    except Exception as e:
        st.error(f"Erro técnico ao salvar no banco: {e}")
        return False
