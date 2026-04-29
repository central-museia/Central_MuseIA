import streamlit as st
st.write("DEBUG:", st.secrets)
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
        <h1 style="font-size:46px;">Resolva o que você precisa agora</h1>
        <p style="font-size:20px;">
        Sem complicação. Sem precisar entender tecnologia.
        </p>
        <p style="font-size:16px; opacity:0.8;">
        Escolha um agente e deixe a MuseIA fazer por você
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
    st.markdown("## 👤 Para você")
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
    st.markdown("## 📦 O que você precisa")
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
    {
        "pergunta": "O que a MuseIA faz por mim?",
        "resposta": "A MuseIA te ajuda a resolver tarefas do dia a dia de forma rápida. Você escolhe o que precisa e o agente faz por você."
    },
    {
        "pergunta": "Preciso saber usar inteligência artificial?",
        "resposta": "Não precisa. Tudo já está pronto. Você só escolhe o que quer fazer e segue os passos."
    },
    {
        "pergunta": "Isso realmente funciona?",
        "resposta": "Sim. Cada agente foi criado para resolver um problema específico, de forma simples e prática."
    },
    {
        "pergunta": "Vou economizar tempo mesmo?",
        "resposta": "Sim. Coisas que levariam horas podem ser feitas em poucos minutos com ajuda da MuseIA."
    },
    {
        "pergunta": "Preciso pagar para começar?",
        "resposta": "Você paga apenas quando quiser usar. Sem assinatura e sem compromisso."
    },
    {
        "pergunta": "Posso usar mais de um agente?",
        "resposta": "Sim. Durante o período de acesso, você pode usar diferentes agentes conforme sua necessidade."
    },
    {
        "pergunta": "Meus dados estão seguros?",
        "resposta": "Sim. Seus dados são tratados com segurança e não são compartilhados."
    }
]

    for item in faqs:
        with st.expander(item["pergunta"]):
            st.write(item["resposta"])
    # Adicione isso logo após o loop do FAQ
    st.write("---")
    st.write("### Ainda tem dúvidas?")
    if st.button("Fale com nosso Suporte 📩", use_container_width=True):
        st.switch_page(pag_contato) # Aqui usamos a variável que definimos no passo 3

        # FOOTER
    st.divider()
    st.caption("MuseIA@2026 - Brasil 🇧🇷")


# =========================================
# 3. DEFINIÇÃO DAS VARIÁVEIS DE PÁGINA
# =========================================
# Definimos TUDO primeiro para o Python não se perder
pag_home = st.Page(minha_home, title="MuseIA", icon="🏠", default=True)
pag_agentes = st.Page("pages/agentes.py", title="Agentes", icon="🤖")
pag_login = st.Page("pages/login.py", title="Login", icon="🔑")
pag_pagamento = st.Page("pages/pagamento.py", title="Pagamento", icon="💳")
pag_redefinir = st.Page("pages/redefinir.py", title="Mudar minha senha", icon="🛡️")
pag_contato = st.Page("pages/contato.py", title="Fale Conosco", icon="📩")

# Esta é a página que o botão "Abrir" precisa, mas que não vai ter título no menu
pag_detalhes = st.Page("pages/_agente.py", title="Detalhes do Agente")

# =========================================
# 4. MAPEAMENTO DO MENU (APENAS UM BLOCO)
# =========================================
# Aqui organizamos o que aparece e o que fica escondido
pg = st.navigation({
    "Principal": [
        pag_home, 
        pag_agentes,
        pag_contato
    ],
    "Minha Conta": [
        pag_login,
        pag_pagamento,
        pag_redefinir
    ],
    # O segredo: a chave " " registra a página Detalhes mas não cria rótulo no menu
    " ": [pag_detalhes] 
})

# =========================================
# 5. EXECUÇÃO ÚNICA
# =========================================
# Esse comando deve aparecer APENAS UMA VEZ no arquivo inteiro
pg.run()
