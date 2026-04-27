import streamlit as st

# Configuração da página
st.set_page_config(page_title="Fale Conosco | MuseIA", layout="wide")

# Estilização para manter o padrão MuseIA
st.markdown("""
    <style>
        .main .block-container {
            max-width: 800px;
            padding-top: 2rem;
        }
        .info-box {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #ff4b4b;
            margin-bottom: 25px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📩 Fale Conosco")
st.write("Dúvidas, sugestões ou suporte técnico? Nossa equipe está pronta para ajudar.")

# --- SEÇÃO DE INFORMAÇÕES ---
st.markdown(f"""
    <div class="info-box">
        <p><strong>🕒 Horário de Atendimento:</strong> Segunda a Sexta, das 08h às 16h.</p>
        <p><strong>📧 E-mail Direto:</strong> <a href="mailto:contato.museia@gmail.com">contato.museia@gmail.com</a></p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- FORMULÁRIO DE CONTATO ---
st.subheader("Enviar Mensagem")

# Usando FormSubmit para direcionar ao seu e-mail
# Substitua pelo seu e-mail oficial
email_destino = "contato.museia@gmail.com"

form_html = f"""
    <form action="https://formsubmit.co/{email_destino}" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="https://museia.streamlit.app/contato"> 
        
        <label>Seu Nome:</label><br>
        <input type="text" name="name" placeholder="Como podemos te chamar?" required style="width: 100%; border-radius: 5px; border: 1px solid #ccc; padding: 10px; margin-bottom: 15px;">
        
        <label>Seu E-mail:</label><br>
        <input type="email" name="email" placeholder="Para onde enviamos a resposta?" required style="width: 100%; border-radius: 5px; border: 1px solid #ccc; padding: 10px; margin-bottom: 15px;">
        
        <label>Mensagem:</label><br>
        <textarea name="message" placeholder="Descreva como podemos te ajudar..." required style="width: 100%; height: 150px; border-radius: 5px; border: 1px solid #ccc; padding: 10px; margin-bottom: 15px;"></textarea>
        
        <button type="submit" style="background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold;">
            Enviar Mensagem 🚀
        </button>
    </form>
"""

st.markdown(form_html, unsafe_allow_html=True)

# Rodapé simples
st.write("")
st.caption("MuseIA Digital - Inteligência Artificial para Empreendedores.")
