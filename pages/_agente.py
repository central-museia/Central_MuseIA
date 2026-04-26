from utils.pdf import exportar_resultado_pdf
from utils.factory import executar_agente
from utils.pdf import ler_arquivo

import streamlit as st
from datetime import datetime
import time
import requests

# ✅ P1 — CONFIGURAÇÃO CORRETA NO TOPO
st.set_page_config(layout="wide")

# Inicialização silenciosa
if "resultado_final" not in st.session_state:
    st.session_state.resultado_final = None
if "input_provisorio" not in st.session_state:
    st.session_state.input_provisorio = ""

st.markdown("""
    <style>
        .main .block-container {
            max-width: 95% !important; 
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        .stApp {
            margin: 0 auto;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================
# CONFIGURAÇÃO E ESTADO INICIAL
# =========================================
ag = st.session_state.get("agente_selecionado")

if not ag:
    st.warning("Selecione um agente primeiro.")
    st.switch_page("pages/agentes.py") 
    st.stop()

if "processamento_liberado" not in st.session_state:
    st.session_state.processamento_liberado = False

# =========================================
# EXIBIÇÃO DO AGENTE (DESIGN LIMPO)
# =========================================
col_img, col_txt = st.columns([1, 2])

BASE_URL = "https://lmlfeizxwnhqebotfzsm.supabase.co/storage/v1/object/public/museia-assets/"

def imagem_valida(url):
    try:
        r = requests.get(url, timeout=3)
        return r.status_code == 200
    except:
        return False

url_img = ag.get("url_publica")
if url_img and not url_img.startswith("http"):
    url_img = BASE_URL + url_img

fallback_logo = BASE_URL + "identidade_visual/logo_coringa.webp"

with col_img:
    if url_img and imagem_valida(url_img):
        st.image(url_img, width=250)
    else:
        st.image(fallback_logo, use_container_width=True)

with col_txt:
    st.title(ag.get("nome"))
    st.write(ag.get("descricao"))

# BENEFÍCIOS
conteudo_beneficios = ag.get("beneficios")
if conteudo_beneficios:
    st.markdown(f"### ⚡ Benefícios do {ag.get('nome')}")
    lista_beneficios = [b.strip() for b in conteudo_beneficios.split("|") if b.strip()]
    for item in lista_beneficios:
        st.markdown(f"- {item}")
else:
    st.markdown("### ⚡ Benefícios")
    st.markdown("- Entrega de alta performance\n- Padrão de qualidade MuseIA")

# BOTÃO DE AÇÃO
if not st.session_state.processamento_liberado:
    if st.button("🚀 Usar este agente", use_container_width=True, key=f"btn_usar_{ag.get('id')}"):
        st.session_state.processamento_liberado = True
        st.rerun()

# =========================================
# ÁREA DE TRABALHO (REAJUSTADA)
# =========================================
if st.session_state.processamento_liberado:
    
    # 1. STATUS
    logado = st.session_state.get("logado", False)
    usuario = st.session_state.get("usuario", {})
    plano_ativo = usuario.get("ativo", False) if logado else False

    if logado:
        st.session_state.origem = None

    if not logado:
        col_aviso, col_btn = st.columns([3, 1])
        with col_aviso:
            st.warning("🔒 **Modo Visualização:** Faça login para processar arquivos.")
        with col_btn:
            if st.button("Fazer Login 🔑", use_container_width=True):
                st.session_state.origem = "pages/_agente.py"
                st.switch_page("pages/login.py")
                st.stop()

    elif not plano_ativo:
        col_aviso, col_btn = st.columns([3, 1])
        with col_aviso:
            st.error("⚠️ **Plano Inativo:** Renove para gerar resultados.")
        with col_btn:
            if st.button("Renovar Plano 💳", use_container_width=True):
                st.switch_page("pages/pagamento.py")
                st.stop()
    else:
        st.success(f"✅ **Tudo pronto!** Você está usando o robô: **{ag.get('nome')}**")

    # CONFIG (VARIÁVEIS QUE O INPUT PRECISA)
    regras = ag.get('regras_processamento', {})
    codigo_python = ag.get("codigo_python")

    if "resultado_gerado" not in st.session_state:
        st.session_state.resultado_gerado = False
    if "executar_agora" not in st.session_state:
        st.session_state.executar_agora = False
    if "input_execucao" not in st.session_state:
        st.session_state.input_execucao = None

    # =========================================
    # MODO INPUT (DENTRO DO BLOCO DE TRABALHO)
    # =========================================
    if not st.session_state.resultado_gerado:
        arquivo_upload = st.file_uploader(
            "📂 Envie um arquivo (PDF, CSV ou TXT)", 
            type=["pdf", "csv", "txt"]
        )
        
        dados_input = st.text_area(
            "📋 Ou cole aqui as informações...", 
            value=st.session_state.input_provisorio,
            height=200
        )
        
        col_run, col_clear = st.columns([1, 1])
        
        with col_run:
            if st.button("🪄 Gerar Resultado Agora", use_container_width=True):
                st.session_state.input_provisorio = dados_input

                if not dados_input and not arquivo_upload:
                    st.warning("Por favor, insira um texto ou envie um arquivo.")
                else:
                    with st.spinner("Processando..."):
                        time.sleep(1)
                        texto_para_processar = ler_arquivo(arquivo_upload) if arquivo_upload else dados_input
                        st.session_state.input_execucao = texto_para_processar
                        st.session_state.executar_agora = True
                        st.session_state.resultado_gerado = True
                        st.session_state.input_provisorio = ""
                        st.rerun()

    # =========================================
    # MODO RESULTADO (DENTRO DO BLOCO DE TRABALHO)
    # =========================================
    else:
        if st.session_state.executar_agora:
            executar_agente(st.session_state.input_execucao, regras, codigo_python)
            st.session_state.executar_agora = False
            st.success("Resultado gerado!")

        if st.button("🔄 Gerar novo resultado", use_container_width=True):
            st.session_state.resultado_gerado = False
            st.session_state.executar_agora = False
            st.rerun()

# =========================================
# BOTÃO VOLTAR (FORA DO BLOCO DE TRABALHO)
# =========================================
st.write("") 

if st.button("⬅ Voltar para Galeria", key="btn_voltar_unico"):
    st.session_state.agente_selecionado = None 
    st.session_state.processamento_liberado = False
    st.session_state.resultado_gerado = False
    st.session_state.resultado_final = None
    st.session_state.input_provisorio = "" 
    st.switch_page("pages/agentes.py")

