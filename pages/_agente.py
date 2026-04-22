from utils.pdf import exportar_resultado_pdf
from utils.factory import executar_agente
from utils.pdf import ler_arquivo

import streamlit as st
from datetime import datetime
import time

# ✅ P1 — CONFIGURAÇÃO CORRETA NO TOPO
st.set_page_config(layout="wide")

# Inicialização silenciosa (Obrigatória para o Streamlit não travar na largada)
if "resultado_final" not in st.session_state:
    st.session_state.resultado_final = None

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
col_img, col_txt = st.columns([2, 2])

with col_img:
    st.image(ag.get("url_publica") or "https://via.placeholder.com/400", use_container_width=True)

with col_txt:
    st.title(ag.get("nome"))
    st.write(ag.get("descricao"))

# =========================================
# EXIBIÇÃO DINÂMICA DE BENEFÍCIOS (BANCO DE DADOS)
# =========================================

conteudo_beneficios = ag.get("beneficios")

if conteudo_beneficios:
    st.markdown(f"### ⚡ Benefícios do {ag.get('nome')}")

    # ✅ P2 — SPLIT BLINDADO
    lista_beneficios = [b.strip() for b in conteudo_beneficios.split("|") if b.strip()]

    for item in lista_beneficios:
        st.markdown(f"- {item}")

else:
    st.markdown("### ⚡ Benefícios")
    st.markdown("- Entrega de alta performance\n- Padrão de qualidade MuseIA")

# =========================================
# BOTÃO DE AÇÃO (LÓGICA DE ACESSO)
# =========================================

if not st.session_state.get("processamento_liberado"):
    if st.button("🚀 Usar este agente", use_container_width=True, key=f"btn_usar_{ag.get('id')}"):
        
        if not st.session_state.get("logado"):
            st.session_state.origem = "pages/_agente.py"
            st.warning("Identificamos que você não está logada. Redirecionando...")
            time.sleep(1)
            st.switch_page("pages/login.py")
            st.stop()

        user = st.session_state.get("usuario")
        
        if user:
            hoje = datetime.now().date()
            data_exp_str = user.get("data_expiracao")
            
            try:
                expiracao = datetime.strptime(data_exp_str, '%Y-%m-%d').date() if data_exp_str else hoje
                
                if not user.get("ativo") or hoje > expiracao:
                    st.error("Seu acesso expirou ou não está ativo.")
                    st.info("Redirecionando para a página de renovação...")
                    time.sleep(2)
                    st.switch_page("pages/pagamento.py")
                    st.stop()
                
                else:
                    st.success(f"Acesso liberado! Bem-vinda.")
                    st.session_state.processamento_liberado = True
                    
            except Exception as e:
                st.error("Erro ao validar dados. Por favor, faça login novamente.")
                st.session_state.logado = False

# =========================================
# ÁREA DE TRABALHO (APARECE APÓS VALIDAÇÃO)
# =========================================
if st.session_state.processamento_liberado:
    st.info(f"Você está usando o robô: **{ag.get('nome')}**")
    
    regras = ag.get('regras_processamento', {})
    codigo_python = ag.get("codigo_python")

    if "resultado_gerado" not in st.session_state:
        st.session_state.resultado_gerado = False

    if "executar_agora" not in st.session_state:
        st.session_state.executar_agora = False

    if "input_execucao" not in st.session_state:
        st.session_state.input_execucao = None

    # =========================================
    # MODO INPUT
    # =========================================
    if not st.session_state.resultado_gerado:

        arquivo_upload = st.file_uploader(
            "📂 Envie um arquivo (PDF, CSV ou TXT)", 
            type=["pdf", "csv", "txt"]
        )
        
        dados_input = st.text_area(
            "📋 Ou cole aqui as informações para o agente analisar:", 
            height=200
        )
        
        col_run, col_clear = st.columns([1, 1])
        
        with col_run:
            if st.button("🪄 Gerar Resultado Agora", use_container_width=True):
                if dados_input or arquivo_upload:
                    with st.spinner("A MuseIA está processando sua solicitação..."):
                        time.sleep(1)

                        if arquivo_upload:
                            texto_para_processar = ler_arquivo(arquivo_upload)
                        else:
                            texto_para_processar = dados_input

                        st.session_state.input_execucao = texto_para_processar
                        st.session_state.executar_agora = True
                        st.session_state.resultado_gerado = True

                        st.rerun()

                else:
                    st.warning("Por favor, insira um texto ou envie um arquivo.")

    # =========================================
    # MODO RESULTADO
    # =========================================
    else:

        # ✅ P4 — SUCESSO NO MOMENTO CERTO
        if not st.session_state.executar_agora:
            st.success("Resultado gerado com sucesso!")

        # 🔥 EXECUÇÃO CONTROLADA
        if st.session_state.executar_agora:
            executar_agente(
                st.session_state.input_execucao,
                regras,
                codigo_python
            )
            st.session_state.executar_agora = False

        if st.button("🔄 Gerar novo resultado", use_container_width=True):
            st.session_state.resultado_gerado = False
            st.session_state.executar_agora = False
            st.session_state.input_execucao = None
            st.rerun()

# =========================================
# BOTÃO VOLTAR
# =========================================
st.write("") 

if st.button("⬅ Voltar para Galeria", key="btn_voltar_unico"):
    st.session_state.agente_selecionado = None 
    st.session_state.processamento_liberado = False
    st.session_state.resultado_final = None
    st.switch_page("pages/agentes.py")
