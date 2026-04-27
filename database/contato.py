from supabase import create_client
import streamlit as st


# 🔧 CONFIG
st.set_page_config(page_title="Fale Conosco | MuseIA", layout="centered")

# 🔌 CONEXÃO
def get_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)
    
except Exception:
    st.error("Erro de Configuração: Chaves do Supabase não encontradas.")
    st.stop()

# 💾 INSERT
def inserir_mensagem_contato(nome, email, assunto, mensagem):
    try:
        supabase = get_client()

        dados = {
            "nome": nome,
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem,
            "status": "Pendente"
        }

        resposta = supabase.table("fale_conosco").insert(dados).execute()

        st.write(resposta)  # 👈 diagnóstico real

        return bool(resposta.data)

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
