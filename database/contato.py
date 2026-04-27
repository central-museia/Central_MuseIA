import streamlit as st
from supabase import create_client

# Função para inicializar o cliente Supabase usando st.secrets (padrão Streamlit)
def get_supabase_client():
    # Se você estiver usando .env localmente, o Streamlit também lê via secrets
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def inserir_mensagem_contato(nome, email, assunto, mensagem):
    try:
        supabase = get_supabase_client()
        
        dados = {
            "nome": nome,
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem,
            "status": "Pendente"
        }
        
        # O .execute() no Supabase Python v2 retorna o objeto de dados
        supabase.table("fale_conosco").insert(dados).execute()
        return True
        
    except Exception as e:
        # Isso ajuda você a ver o erro real no console se algo falhar
        st.error(f"Erro técnico ao salvar no banco: {e}")
        return False
