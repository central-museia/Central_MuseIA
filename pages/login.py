import streamlit as st
import time
from database.cliente import validar_login, cadastrar_usuario, recuperar_senha

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Acesso | MuseIA", layout="centered", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #e50914;'>MuseIA Digital</h1>", unsafe_allow_html=True)

# 2. CRIAÇÃO DAS ABAS
aba_login, aba_cadastro, aba_recuperar = st.tabs(["🔐 Entrar", "📝 Cadastrar", "🔑 Esqueci a Senha"])

# --- ABA DE LOGIN ---
with aba_login:
    with st.form("login_form"):
        email = st.text_input("E-mail").lower().strip()
        senha = st.text_input("Senha", type="password")
        btn_login = st.form_submit_button("Acessar Central")
        
        if btn_login:
            user = validar_login(email, senha)
            if user:
                # 1. Salva os dados na sessão
                st.session_state.logado = True
                st.session_state.usuario = user
                st.success(f"Bem-vinda, {user.get('nome')}!")
                time.sleep(1)
                
                # 2. LÓGICA DE REDIRECIONAMENTO (DENTRO DO SUCESSO DO LOGIN)
                pagina_retorno = st.session_state.get("origem")

                if pagina_retorno:
                    st.session_state.origem = None # Limpa o rastro
                    try:
                        st.switch_page(pagina_retorno)
                    except:
                        st.switch_page("pages/_agente.py")
                else:
                    # Se não veio de um agente específico, vai para a vitrine
                    st.switch_page("pages/agentes.py")
            else:
                st.error("E-mail ou senha incorretos.")

# --- ABA DE CADASTRO ---
with aba_cadastro:
    with st.form("cadastro_form"):
        novo_nome = st.text_input("Nome Completo")
        novo_email = st.text_input("E-mail").lower().strip()
        nova_senha = st.text_input("Crie uma Senha", type="password")
        confirma_senha = st.text_input("Confirme a Senha", type="password")
        
        btn_cadastrar = st.form_submit_button("Criar minha Conta")
        
        if btn_cadastrar:
            if nova_senha != confirma_senha:
                st.error("As senhas não conferem.")
            elif len(nova_senha) < 6:
                st.warning("A senha deve ter no mínimo 6 caracteres.")
            else:
                sucesso, msg = cadastrar_usuario(novo_nome, novo_email, nova_senha)
                if sucesso:
                    st.success("Conta criada! Agora você pode fazer login.")
                else:
                    st.error(f"Erro ao cadastrar: {msg}")

# --- ABA DE RECUPERAÇÃO ---
with aba_recuperar:
    st.write("Enviaremos instruções para o seu e-mail cadastrado.")
    email_recupera = st.text_input("Digite seu e-mail de cadastro").lower().strip()
    
    if st.button("Solicitar Nova Senha"):
        if email_recupera:
            with st.spinner("Processando solicitação..."):
                sucesso, msg = recuperar_senha(email_recupera)
                if sucesso:
                    st.info("Se este e-mail estiver na nossa base, você receberá um link de redefinição.")
                else:
                    st.error("Erro ao processar solicitação.")
        else:
            st.warning("Informe o e-mail.")

# --- BLOCO PADRONIZADO DE RETORNO ---
st.markdown("---")
if st.button("🏠 Voltar para a Vitrine"):
    # Usamos o caminho relativo do arquivo principal. 
    # Se o seu arquivo principal se chama streamlit_app.py, é este o comando:
    st.switch_page("streamlit_app.py")
