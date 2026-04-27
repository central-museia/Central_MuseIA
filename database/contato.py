import streamlit as st
from supabase import create_client


# 🔌 CONEXÃO
def get_supabase_contato():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar no Supabase: {e}")
        return None


# 💾 INSERT
def inserir_mensagem_contato(nome, email, assunto, mensagem):
    
    # 🔒 validação mínima (evita lixo e erro silencioso)
    if not nome or not email or not mensagem:
        st.warning("Preencha os campos obrigatórios.")
        return False

    try:
        supabase = get_supabase_contato()

        if not supabase:
            return False

        dados = {
            "nome": nome,
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem,
            "status": "Pendente"
        }

        # 🚨 EXECUTA E GUARDA RESPOSTA
        resposta = supabase.table("fale_conosco").insert(dados).execute()

        # ✅ VALIDA SE INSERIU MESMO
        if hasattr(resposta, "data") and resposta.data:
            return True
        else:
            st.error(f"Erro ao inserir (resposta vazia): {resposta}")
            return False

    except Exception as e:
        st.error(f"Erro técnico ao salvar no banco: {e}")
        return False
