from utils.pdf import exportar_resultado_pdf
from utils.factory import executar_agente
from utils.pdf import ler_arquivo

import streamlit as st
from datetime import datetime
import time

# Inicialização silenciosa (Obrigatória para o Streamlit não travar na largada)
if "resultado_final" not in st.session_state:
    st.session_state.resultado_final = None

def sua_funcao_do_agente(): # Procure o início da função da página
    # 1. ESTA DEVE SER A PRIMEIRA LINHA DE CÓDIGO DENTRO DA FUNÇÃO
  st.set_page_config(layout="wide") # ISSO AQUI É OBRIGATÓRIO

st.markdown("""
    <style>
        /* Isso aqui LIBERA a página, não engessa. Pode manter! */
        .main .block-container {
            max-width: 95% !important; 
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        /* Remove o topo vazio */
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

with col_img:
    st.image(ag.get("url_publica") or "https://via.placeholder.com/400", use_container_width=True)

with col_txt:
    st.title(ag.get("nome"))
    st.write(ag.get("descricao"))

st.markdown("### ⚡ Benefícios")
st.markdown("""
- Economiza tempo real na sua operação
- Automatiza tarefas repetitivas
- Reduz erros humanos e aumenta a produtividade
""")

st.divider()

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

    if "resultado_final" not in st.session_state:
        st.session_state.resultado_final = None

    arquivo_upload = st.file_uploader("📂 Envie um arquivo (PDF, CSV ou TXT)", type=["pdf", "csv", "txt"])
    
    dados_input = st.text_area("📋 Ou cole aqui as informações para o agente analisar:", height=200)
    
    col_run, col_clear = st.columns([1, 1])
    
    with col_run:
        if st.button("🪄 Gerar Resultado Agora", use_container_width=True):
            if dados_input or arquivo_upload:
                with st.spinner("A MuseIA está processando sua solicitação..."):
                    time.sleep(1)

                    # 🔹 PROCESSAMENTO REAL
                    if arquivo_upload:
                        texto_para_processar = ler_arquivo(arquivo_upload)
                    else:
                        texto_para_processar = dados_input

                    resultado_tratado = executar_agente(
                        texto_para_processar,
                        regras,
                        codigo_python
                    )

                    st.session_state.resultado_final = (
                        f"RESULTADO DA MUSEIA\n---\n"
                        f"Agente: {ag.get('nome')}\n"
                        f"Data: {datetime.now().strftime('%d/%m/%Y')}\n---\n\n"
                        f"{resultado_tratado}"
                    )
            else:
                st.warning("Por favor, insira um texto ou envie um arquivo.")
                
# =========================================
# ✅ ENTREGA (SÓ APARECE APÓS O PROCESSAMENTO)
# =========================================
if st.session_state.resultado_final:
    st.divider()
    st.markdown("### ✅ Resultado Processado")
    
    resultado_texto = st.session_state.resultado_final
    st.text_area("", resultado_texto, height=300)
    
    try:
        nome_do_agente = ag.get('nome', 'Agente_MuseIA')
        
        pdf_bytes = exportar_resultado_pdf(resultado_texto, nome_do_agente)
        
        st.download_button(
            label="📥 Clique aqui para salvar o arquivo",
            data=pdf_bytes,
            file_name=f"MuseIA_{nome_do_agente}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Erro ao preparar o PDF: {e}")

# =========================================
# BOTÃO VOLTAR
# =========================================
st.write("") 
if st.button("⬅ Voltar para Galeria", key="btn_voltar_unico"):
    st.session_state.agente_selecionado = None 
    st.session_state.processamento_liberado = False
    st.session_state.resultado_final = None
    st.switch_page("pages/agentes.py")
