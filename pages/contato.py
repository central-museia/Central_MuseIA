import streamlit as st

# Configuração da página
st.set_page_config(page_title="Fale Conosco | MuseIA", layout="wide")

# Estilização ajustada para Dark Mode
st.markdown("""
    <style>
        .main .block-container {
            max-width: 900px;
            padding-top: 2rem;
        }
        /* Box de informações com texto escuro garantido */
        .info-box {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 15px;
            border-left: 8px solid #ff4b4b;
            margin-bottom: 30px;
            color: #1f1f1f !important; /* Força o texto a ficar escuro */
        }
        .info-box p {
            margin-bottom: 8px;
            font-size: 1.1rem;
            color: #1f1f1f !important;
        }
        /* Estilo dos inputs para combinar com o tema dark */
        .st-form-input {
            width: 100%;
            border-radius: 8px;
            border: 1px solid #444;
            padding: 12px;
            margin-bottom: 20px;
            background-color: #262730;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📩 Fale com a MuseIA")
st.write("Precisa de ajuda, suporte ou quer falar com a gente? Responda rápido e direto.")

# --- SEÇÃO DE INFORMAÇÕES (TEXTO CORRIGIDO) ---
st.markdown(f"""
    <div class="info-box">
        <p><strong>🕒 Horário de Atendimento:</strong> Segunda a Sexta, das 08h às 16h.</p>
        <p><strong>📧 E-mail Direto:</strong> <a href="mailto:contato.museia@gmail.com" style="color: #ff4b4b; text-decoration: none; font-weight: bold;">contato.museia@gmail.com</a></p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- FORMULÁRIO DE CONTATO ---
st.subheader("✉️ Enviar mensagem")

with st.form("form_contato"):
    assunto = st.selectbox(
        "Como podemos te ajudar?",
        [
            "Suporte Técnico (Erro ou Acesso)",
            "Financeiro / Pagamentos",
            "Dúvidas sobre os Agentes",
            "Parcerias e Afiliados",
            "Trabalhe Conosco",
            "Sugestões de novos Robôs",
            "Outros"
        ]
    )
    nome = st.text_input("Seu nome")
    email = st.text_input("Seu e-mail")
    mensagem = st.text_area("Mensagem", height=150)

    enviar = st.form_submit_button("Enviar mensagem 🚀")

    if enviar:
        if not nome or not email or not mensagem:
            st.warning("Preencha todos os campos.")
        else:
            # Aqui você pode integrar depois com API, email, etc
            st.success("Mensagem enviada com sucesso! Retornaremos em breve.")

st.write("")
st.caption("MuseIA Digital - A inteligência humana que controla a IA.")
