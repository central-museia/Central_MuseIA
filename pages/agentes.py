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
# 5. VITRINE ESTILO NETFLIX COM LOGO MUSEIA
# =========================================

# URL da sua logo oficial (Coringa/Fallback)
fallback_logo = "https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/identidade_visual/logo_coringa.webp"

# Estilização para garantir que a Logo não fique esticada
st.markdown("""
    <style>
    [data-testid="stImage"] img {
        border-radius: 12px;
        object-fit: cover;
        height: 140px !important; 
        border: 1px solid #1e1e1e; /* Borda sutil para dar profundidade */
    }
    </style>
""", unsafe_allow_html=True)

if not agentes_filtrados:
    st.info("Nenhum agente encontrado.")
else:
    num_colunas = 5 
    cols = st.columns(num_colunas)

    for i, ag in enumerate(agentes_filtrados):
        with cols[i % num_colunas]:
            
            # 🔹 LÓGICA DE IMAGEM: Se 'url_publica' for nula ou vazia, usa a Logo MuseIA
            url_img = ag.get("url_publica")
            
            # Validação profissional: verifica se a URL existe e não é apenas um espaço
            if url_img and str(url_img).strip():
                img_exibir = url_img
            else:
                img_exibir = "https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/identidade_visual/logo_coringa.webp"
            
            # Renderização da Capa do Agente
            st.image(img_exibir, use_container_width=True)

            # 🔹 TÍTULO DO AGENTE (Abaixo da imagem)
            st.markdown(f"<p style='font-size: 13px; font-weight: 600; margin-top: 5px; color: #f0f0f0;'>{ag.get('nome')}</p>", unsafe_allow_html=True)
            
            # 🔹 BOTÃO DE ACESSO (O gatilho para a página _agente.py)
            if st.button("Abrir", key=f"ag_{ag.get('id')}", use_container_width=True):
                st.session_state.agente_selecionado = ag
                st.switch_page("pages/_agente.py")
