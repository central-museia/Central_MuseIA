import streamlit as st
from supabase import create_client

# 🔧 CONFIG
st.set_page_config(page_title="Fale Conosco | MuseIA", layout="centered")

# 🔌 CONEXÃO
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

# 💾 INSERT
def inserir_mensagem(nome, email, assunto, mensagem):
    try:
        supabase = get_supabase()

        dados = {
            "nome": nome,
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem,
            "status": "Pendente"
        }

        resposta = supabase.table("fale_conosco").insert(dados).execute()

        if resposta.data:
            return True
        else:
            st.error(f"Erro ao salvar: {resposta}")
            return False

    except Exception as e:
        st.error(f"Erro técnico: {e}")
        return False


# 🎨 UI
st.title("📩 Fale Conosco")
st.write("Nos envie uma mensagem e retornaremos o mais rápido possível.")

st.divider()

# 🧾 FORMULÁRIO REAL (STREAMLIT)
with st.form("form_contato"):

    nome = st.text_input("Seu nome")
    email = st.text_input("Seu e-mail")

    assunto = st.selectbox(
        "Assunto",
        [
            "Suporte Técnico",
            "Dúvida",
            "Sugestão",
            "Financeiro",
            "Outro"
        ]
    )

    mensagem = st.text_area("Mensagem", height=150)

    enviar = st.form_submit_button("Enviar Mensagem 🚀")

    if enviar:

        # 🔒 validação simples
        if not nome or not email or not mensagem:
            st.warning("Preencha os campos obrigatórios.")
        else:
            sucesso = inserir_mensagem(nome, email, assunto, mensagem)

            if sucesso:
                st.success("Mensagem enviada com sucesso!")
                st.balloons()
            else:
                st.error("Não foi possível enviar. Tente novamente.")
