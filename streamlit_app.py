import streamlit as st
import os
import sys

# =========================================
# 1. PATH + CONFIG (TOPO ABSOLUTO)
# =========================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

st.set_page_config(
    page_title="MuseIA Digital", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# 2. HOME ISOLADA (SEU CÓDIGO REAL AQUI)
# =========================================
def minha_home():

    import unicodedata
    import time
    from database.catalogo import obter_agentes, obter_perfis, obter_colecoes
    from database.cliente import validar_login

    # =========================================
    # SESSION (Inicialização garantida)
    # =========================================
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

    # =========================================
    # FUNÇÕES AUXILIARES
    # =========================================
    def normalizar(texto):
        if not texto: return ""
        return unicodedata.normalize('NFKD', str(texto)).encode('ascii', 'ignore').decode('utf-8').lower()

    # =========================================
    # CSS CUSTOMIZADO (ORIGINAL)
    # =========================================
    st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; padding-bottom: 0rem !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0.5rem; align-items: center; }
    div[data-testid="stVerticalBlock"] > div { padding-top: 0rem; padding-bottom: 0rem; }
    button { padding: 0.25rem 0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

    # =========================================
    # CARREGAMENTO DE DADOS
    # =========================================
    perfis_db = obter_perfis() or []
    colecoes_db = obter_colecoes() or []
    agentes_db = obter_agentes() or []

    # =========================================
    # HEADER
    # =========================================
    col1, col2 = st.columns([4,1])

    with col1:
        st.image(
            "https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/identidade_visual/logo_coringa.webp",
            width=80
        )

    with col2:
        if st.session_state.logado:
            nome_curto = st.session_state.usuario.get('nome', 'Usuário').split()[0]
            st.write(f"Olá, **{nome_curto}**!")
            if st.button("Sair", use_container_width=True):
                st.session_state.logado = False
                st.session_state.usuario = {}
        else:
            c_login, c_cadastro = st.columns(2)
            with c_login:
                if st.button("Entrar", use_container_width=True):
                    st.switch_page("pages/login.py")
            with c_cadastro:
                if st.button("Cadastrar", use_container_width=True):
                    st.switch_page("pages/login.py")

    # =========================================
    # HERO
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
    # BUSCA
    # =========================================
    busca = st.text_input("", placeholder="O que você deseja resolver?", label_visibility="collapsed")

    if busca:
        resultados = [a for a in agentes_db if busca.lower() in (a.get("nome") or "").lower()]
        if resultados:
            st.session_state.agente_selecionado = resultados[0]
            st.switch_page("pages/agentes.py")

    # RESET FILTROS
    if st.session_state.get("reset_filtros"):
        st.session_state.filtro_perfil = None
        st.session_state.filtro_colecao = None
        st.session_state.reset_filtros = False

    # =========================================
    # PERFIS
    # =========================================
    st.markdown("## 👤 Perfil")
    if perfis_db:
        cols = st.columns(min(len(perfis_db), 6))
        for i, perfil in enumerate(perfis_db):
            nome = perfil if isinstance(perfil, str) else perfil.get("nome")
            with cols[i % 6]:
                if st.button(nome, key=f"perfil_{i}", use_container_width=True):
                    st.session_state.filtro_perfil = nome
                    st.session_state.filtro_colecao = "Todos"
                    st.switch_page("pages/agentes.py")

    # =========================================
    # COLEÇÕES
    # =========================================
    st.markdown("## 📦 Coleções")
    if colecoes_db:
        cols = st.columns(min(len(colecoes_db), 6))
        for i, colecao in enumerate(colecoes_db):
            nome = colecao if isinstance(colecao, str) else colecao.get("nome")
            with cols[i % 6]:
                if st.button(nome, key=f"colecao_{i}", use_container_width=True):
                    st.session_state.filtro_colecao = nome
                    st.session_state.filtro_perfil = "Todos"
                    st.switch_page("pages/agentes.py")

    # =========================================
    # FAQ
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


# =========================================
# 3. NAVEGAÇÃO
# =========================================

# Criamos a definição da página de detalhes, mas NÃO a colocamos no dicionário abaixo.
# Isso faz com que ela exista para o sistema, mas fique invisível no menu lateral.
pag_detalhes = st.Page("pages/_agente.py", title="Detalhes")

pg = st.navigation({
    "Principal": [
        st.Page(minha_home, title="MuseIA", icon="🏠"),
        st.Page("pages/agentes.py", title="Agentes", icon="🤖"),
    ],
    "Minha Conta": [
        st.Page("pages/login.py", title="Login", icon="🔑"),
        st.Page("pages/pagamento.py", title="Pagamento", icon="💳"),
        st.Page("pages/redefinir.py", title="Mudar minha senha", icon="🛡️"),
    ]
})

# =========================================
# 4. EXECUÇÃO
# =========================================
pg.run()
