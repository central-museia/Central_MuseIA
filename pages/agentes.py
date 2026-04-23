import streamlit as st
from database.catalogo import obter_agentes, obter_perfis, obter_colecoes

def normalizar(texto):
    if not texto: return ""
    import unicodedata
    return unicodedata.normalize('NFKD', str(texto)).encode('ascii', 'ignore').decode('utf-8').lower()

st.title("Escolha seu agente")

# 1. CARREGAMENTO DE DADOS
agentes_db = obter_agentes() or []
perfis_db = obter_perfis() or []
colecoes_db = obter_colecoes() or []

# 2. LÓGICA DE SINCRONIZAÇÃO (HOME -> AGENTES)
p_inicial = st.session_state.get("filtro_perfil", "Todos")
c_inicial = st.session_state.get("filtro_colecao", "Todos")

opcoes_perfil = ["Todos"] + perfis_db
opcoes_colecao = ["Todos"] + colecoes_db

# Evita erro de ValueError se o perfil vindo da Home não existir na lista
idx_p = opcoes_perfil.index(p_inicial) if p_inicial in opcoes_perfil else 0
idx_c = opcoes_colecao.index(c_inicial) if c_inicial in opcoes_colecao else 0

# 3. INTERFACE DE BUSCA E FILTROS
busca = st.text_input("", placeholder="Buscar agente...", label_visibility="collapsed")

col1, col2 = st.columns(2)
with col1:
    filtro_perfil = st.selectbox("Perfil", opcoes_perfil, index=idx_p)
    st.session_state.filtro_perfil = filtro_perfil

with col2:
    filtro_colecao = st.selectbox("Coleção", opcoes_colecao, index=idx_c)
    st.session_state.filtro_colecao = filtro_colecao

if filtro_perfil != "Todos" or filtro_colecao != "Todos" or busca:
    if st.button("❌ Limpar Filtros"):
        st.session_state.filtro_perfil = "Todos"
        st.session_state.filtro_colecao = "Todos"

# 4. PROCESSAMENTO DA FILTRAGEM
agentes_filtrados = agentes_db

# Filtro por Texto
if busca:
    agentes_filtrados = [
        a for a in agentes_filtrados 
        if normalizar(busca) in normalizar(a.get("nome", ""))
    ]

# Filtro por Perfil (Lógica N:N ajustada)
if filtro_perfil != "Todos":
    agentes_filtrados = [
        a for a in agentes_filtrados
        if any(
            normalizar(filtro_perfil) == normalizar(p.get("perfis", {}).get("nome", ""))
            for p in a.get("agentes_perfis", []) if p.get("perfis")
        )
    ]

# Filtro por Coleção (Lógica N:N ajustada)
if filtro_colecao != "Todos":
    agentes_filtrados = [
        a for a in agentes_filtrados
        if any(
            normalizar(filtro_colecao) == normalizar(c.get("colecoes", {}).get("nome", ""))
            for c in a.get("agentes_colecoes", []) if c.get("colecoes")
        )
    ]

# =========================================
# 5. EXIBIÇÃO DA VITRINE
# =========================================

fallback_logo = "https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/identidade_visual/logo_coringa.webp"

if not agentes_filtrados:
    st.info("Nenhum agente encontrado para os filtros selecionados.")
else:
    cols = st.columns(3)

    for i, ag in enumerate(agentes_filtrados):
        with cols[i % 3]:

            st.markdown("""
            <div style="
                background-color: #111;
                padding: 15px;
                border-radius: 12px;
                text-align: center;
                height: 100%;
            ">
            """, unsafe_allow_html=True)

            # 🔹 IMAGEM FLEXÍVEL SEGURA
            url_img = ag.get("url_publica") or fallback_logo

            st.markdown(
                "<div style='height:180px; display:flex; align-items:center; justify-content:center;'>",
                unsafe_allow_html=True
            )
            st.image(url_img, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # 🔹 TEXTO
            st.markdown(f"**{ag.get('nome')}**")
            st.caption(f"ID: {ag.get('codigo', 'S/C')}")

            # 🔹 BOTÃO
            if st.button("Acessar", key=f"ag_{ag.get('id')}", use_container_width=True):
                st.session_state.agente_selecionado = ag
                st.switch_page("pages/_agente.py")

            st.markdown("</div>", unsafe_allow_html=True)
