import streamlit as st
from database.catalogo import obter_agentes, obter_perfis, obter_colecoes
import requests

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

fallback_logo = "https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/identidade_visual/logo_coringa.webp"

st.markdown("""
    <style>
    [data-testid="stImage"] img {
        border-radius: 12px;
        object-fit: cover;
        height: 140px !important; 
        border: 1px solid #1e1e1e;
    }
    </style>
""", unsafe_allow_html=True)

if not agentes_filtrados:
    st.info("Nenhum agente encontrado.")
else:
    num_colunas = 5 
    cols = st.columns(num_colunas)

    # AQUI ESTAVA O ERRO: O FOR PRECISA ESTAR ALINHADO DENTRO DO ELSE
for i, ag in enumerate(agentes_filtrados):
        with cols[i % num_colunas]:
            
            # 1. Pega a URL que o banco gerou (ou planos B e C)
            url_gerada = ag.get("url_publica") or ag.get("imagem_url") or ag.get("avatar")
            
            # 2. Função interna para checar se a imagem existe de verdade no Storage
            def validar_link(url):
                if not url or str(url).lower() in ["none", "nan", "", "null"]:
                    return False
                try:
                    # O 'timeout' evita que seu site fique lento se o storage demorar
                    # O 'head' apenas checa se o arquivo existe sem baixar a imagem inteira
                    check = requests.head(url, timeout=0.8)
                    return check.status_code == 200
                except:
                    return False

            # 3. A DECISÃO: Se o link não for real/válido, usa a logo MuseIA
            if validar_link(url_gerada):
                img_exibir = url_gerada
            else:
                img_exibir = fallback_logo

            # 4. Renderização Final
            st.image(img_exibir, use_container_width=True)

          # Título do Agente
            nome_agente = ag.get('nome', 'Agente sem nome')
            st.markdown(f"<p style='font-size: 13px; font-weight: 600; margin-top: 5px; color: #f0f0f0;'>{nome_agente}</p>", unsafe_allow_html=True)
            
            # Botão Abrir (Ajustado com indentação correta)
            if st.button("Abrir", key=f"ag_{ag.get('id', i)}", use_container_width=True):
                # 1. Salva na memória
                st.session_state.agente_selecionado = ag
                
                # 2. Tenta a navegação
                try:
                    # Tenta pelo caminho do arquivo (mais seguro)
                    st.switch_page("pages/_agente.py")
                except:
                    # Se falhar, tenta pelo título que definimos no maestro
                    st.switch_page("pages/_agente.py")
                    # --- BLOCO PADRONIZADO DE RETORNO ---
st.markdown("---")
if st.button("🏠 Voltar para a Vitrine"):
    # Usamos o caminho relativo do arquivo principal. 
    # Se o seu arquivo principal se chama streamlit_app.py, é este o comando:
    st.switch_page("streamlit_app.py")
