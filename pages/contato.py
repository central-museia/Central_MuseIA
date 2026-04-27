import streamlit as st

# CONFIG
st.set_page_config(page_title="Fale Conosco | MuseIA", layout="wide")

# 🎨 ESTILO MUSEIA (mais limpo e profissional)
st.markdown("""
<style>
.main .block-container {
    max-width: 900px;
    padding-top: 2rem;
}

.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #e6e6e6;
    margin-bottom: 20px;
}

.highlight {
    border-left: 5px solid #6C63FF;
    background-color: #f7f7ff;
}

.title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 10px;
}

.subtitle {
    color: #666;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="title">📩 Fale com a MuseIA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Precisa de ajuda, suporte ou quer falar com a gente? Responda rápido e direto.</div>', unsafe_allow_html=True)

# INFO
st.markdown("""
<div class="card highlight">
    <strong>🕒 Atendimento:</strong> Segunda a Sexta, das 08h às 16h<br><br>
    <strong>📧 E-mail:</strong> contato.museia@gmail.com
</div>
""", unsafe_allow_html=True)

# DIVISOR
st.divider()

# FORMULÁRIO NATIVO (MUITO MAIS ESTÁVEL)
st.subheader("✉️ Enviar mensagem")

with st.form("form_contato"):
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

# RODAPÉ
st.divider()
st.caption("MuseIA Digital • Inteligência aplicada para decisões reais")
