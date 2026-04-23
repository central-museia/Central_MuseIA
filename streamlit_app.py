import streamlit as st
import sys
import os
import unicodedata
import time
from database.catalogo import obter_agentes, obter_perfis, obter_colecoes
from database.cliente import validar_login
import streamlit as st
import streamlit as st
# ... todos os seus outros imports (os que você já tinha) ...

# 1. CONFIGURAÇÃO (Obrigatório ser a primeira coisa)
st.set_page_config(
    page_title="MuseIA Digital", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. A FUNÇÃO QUE "ISOLA" A SUA HOME
def mostrar_home():
    # --- TUDO O QUE ERA A SUA PÁGINA PRINCIPAL ENTRA AQUI ---
    # Coloque aqui: Imports internos, Session State, CSS, Hero, Vitrine e FAQ.
    # Exemplo:
    st.image("https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/identidade_visual/logo_coringa.webp", width=80)
    st.markdown('<div class="hero"><h1>Automatize o que te trava</h1></div>', unsafe_allow_html=True)
    # ... todo o resto do seu código ...
    # -------------------------------------------------------

# 3. O MAPA DO MENU (Aqui você define os nomes amigáveis)
pg = st.navigation({
    "Principal": [
        st.Page(mostrar_home, title="MuseIA", icon="🏠"), # Aqui a Home ganha o nome MuseIA
        st.Page("pages/agentes.py", title="Agentes", icon="🤖"),
    ],
    "Minha Conta": [
        st.Page("pages/login.py", title="Login", icon="🔑"),
        st.Page("pages/pagamento.py", title="Pagamento", icon="💳"),
        st.Page("pages/redefinir.py", title="Mudar minha senha", icon="🛡️"),
    ]
})

# 4. O COMANDO ÚNICO DE EXECUÇÃO
# Ele limpa a tela e desenha APENAS o que foi selecionado no menu.
pg.run()

# 2. SESSION (Inicialização garantida)
for key, val in {
    "logado": False,
    "usuario": {},
    "mostrar_auth": False,
    "agente_selecionado": None,
    "filtro_perfil": None,
    "filtro_colecao": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# 3. FUNÇÕES AUXILIARES
def normalizar(texto):
    if not texto: return ""
    return unicodedata.normalize('NFKD', str(texto)).encode('ascii', 'ignore').decode('utf-8').lower()

# CSS CUSTOMIZADO (Mantido original)
st.markdown("""
<style>
.block-container { padding-top: 1.5rem !important; padding-bottom: 0rem !important; }
div[data-testid="stHorizontalBlock"] { gap: 0.5rem; align-items: center; }
div[data-testid="stVerticalBlock"] > div { padding-top: 0rem; padding-bottom: 0rem; }
button { padding: 0.25rem 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# CARREGAMENTO DE DADOS
perfis_db = obter_perfis() or []
colecoes_db = obter_colecoes() or []
agentes_db = obter_agentes() or []

# =========================================
# HEADER (DINÂMICO: LOGIN / NOME DO USUÁRIO)
# =========================================
col1, col2 = st.columns([4,1])

with col1:
    st.image(
        "https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/identidade_visual/logo_coringa.webp",
        width=80
    )

with col2:
    # Se estiver logado, mostra o Nome e o Sair
    if st.session_state.logado:
        nome_curto = st.session_state.usuario.get('nome', 'Usuário').split()[0]
        st.write(f"Olá, **{nome_curto}**!")
        if st.button("Sair", use_container_width=True):
            st.session_state.logado = False
            st.session_state.usuario = {}
            
    # Se não estiver logado, mostra botões de acesso
    else:
        c_login, c_cadastro = st.columns(2)
        with c_login:
            if st.button("Entrar", use_container_width=True):
                st.switch_page("pages/login.py")
        with c_cadastro:
            if st.button("Cadastrar", use_container_width=True):
                st.switch_page("pages/login.py")

# =========================================
# HERO (Mantido original)
# =========================================
st.markdown("""
<style>
.hero {
   background-image: 
        linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
        url('https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/identidade_visual/central_%20de_agentes.webp');
    background-size: cover;
    background-position: center;
    padding: 120px 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
}
</style>
<div class="hero">
    <h1 style="font-size:50px;">Automatize o que te trava</h1>
    <p style="font-size:22px;">Recupere seu tempo com agentes inteligentes</p>
    <p style="font-size:18px; opacity:0.8;">
        Já devolvemos <b>1.284 horas</b> de trabalho repetitivo
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2,1,2])
with c2:
    if st.button("Começar agora", use_container_width=True):
        st.switch_page("pages/agentes.py")

# =========================================
# BUSCA (Mantido original)
# =========================================
busca = st.text_input("", placeholder="O que você deseja resolver?", label_visibility="collapsed")

if busca:
    resultados = [a for a in agentes_db if busca.lower() in (a.get("nome") or "").lower()]
    if resultados:
        st.session_state.agente_selecionado = resultados[0]
        st.switch_page("pages/agentes.py")

# RESET DE FILTROS
if st.session_state.get("reset_filtros"):
    st.session_state.filtro_perfil = None
    st.session_state.filtro_colecao = None
    st.session_state.reset_filtros = False

# =========================================
# PERFIS (Ajustado para limpar coleções ao clicar)
# =========================================
st.markdown("## 👤 Perfil")
if perfis_db:
    cols = st.columns(min(len(perfis_db), 6))
    for i, perfil in enumerate(perfis_db):
        nome = perfil if isinstance(perfil, str) else perfil.get("nome")
        with cols[i % 6]:
            if st.button(nome, key=f"perfil_{i}", use_container_width=True):
                st.session_state.filtro_perfil = nome
                st.session_state.filtro_colecao = "Todos" # <-- Adicione isso
                st.switch_page("pages/agentes.py")

# =========================================
# COLEÇÕES (Ajustado para limpar perfis ao clicar)
# =========================================
st.markdown("## 📦 Coleções")
if colecoes_db:
    cols = st.columns(min(len(colecoes_db), 6))
    for i, colecao in enumerate(colecoes_db):
        nome = colecao if isinstance(colecao, str) else colecao.get("nome")
        with cols[i % 6]:
            if st.button(nome, key=f"colecao_{i}", use_container_width=True):
                st.session_state.filtro_colecao = nome
                st.session_state.filtro_perfil = "Todos" # <-- Adicione isso
                st.switch_page("pages/agentes.py")
                
# =========================================
# FAQ (Mantido original)
# =========================================
st.markdown("## ❓ Dúvidas Frequentes")
faqs = [
    {"pergunta": "O que é a MuseIA?", "resposta": "A MuseIA é uma central de agentes inteligentes..."},
    {"pergunta": "Preciso saber usar IA?", "resposta": "Não. Os agentes já são prontos para uso..."},
    {"pergunta": "Os agentes realmente funcionam?", "resposta": "Sim. Cada agente foi criado para resolver um problema específico..."},
    {"pergunta": "Vou economizar quanto tempo?", "resposta": "Tarefas que levavam horas podem ser feitas em minutos..."},
    {"pergunta": "Preciso pagar para usar?", "resposta": "Acesso completo está disponível para membros."},
    {"pergunta": "Posso usar mais de um agente?", "resposta": "Sim, conforme sua necessidade."},
    {"pergunta": "Meus dados estão seguros?", "resposta": "Sim. A MuseIA utiliza práticas seguras para proteger seus dados."}
]
for item in faqs:
    with st.expander(item["pergunta"]):
        st.write(item["resposta"])

# FOOTER
st.divider()
st.caption("MuseIA@2026 - Brasil 🇧🇷")
