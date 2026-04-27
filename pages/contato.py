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

email_destino = "contato.museia@gmail.com"

form_html = f"""
    <form action="https://formsubmit.co/{email_destino}" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        
        <label style="font-weight: bold;">Seu nome</label><br>
        <input type="text" name="name" class="st-form-input" placeholder="Ex: Deise Maria" required>
        
        <label style="font-weight: bold;">Seu e-mail</label><br>
        <input type="email" name="email" class="st-form-input" placeholder="seuemail@exemplo.com" required>
        
        <label style="font-weight: bold;">Mensagem</label><br>
        <textarea name="message" class="st-form-input" rows="5" placeholder="Como podemos te ajudar?" required style="height: 150px;"></textarea>
        
        <button type="submit" style="background-color: #ff4b4b; color: white; border: none; padding: 15px 30px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; font-size: 1.1rem;">
            Enviar Mensagem Agora 🚀
        </button>
    </form>
"""

st.markdown(form_html, unsafe_allow_html=True)

st.write("")
st.caption("MuseIA Digital - Tecnologia para quem faz.")
