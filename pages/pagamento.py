import streamlit as st
import mercadopago
import os
import time
from datetime import datetime, timedelta
from database.cliente import get_client

st.markdown("""
<style>
    .stApp {
        background-color: #0e0e0e;
    }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE NEGÓCIO ---
PRECO_ACESSO = 49.90
PRECO_REFERENCIA = 79.90  # apenas ancoragem visual
DIAS_ACESSO = 30

NOME_PLANO = "Seu Agente MuseIA"

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Checkout | MuseIA", layout="centered")

# Inicializa o SDK do Mercado Pago usando st.secrets
try:
    token_mp = st.secrets["mercadopago"]["access_token"]
    public_key_mp = st.secrets["mercadopago"]["public_key"]
except Exception:
    st.error("Configuração ausente: Verifique o arquivo .streamlit/secrets.toml")
    st.stop()

sdk = mercadopago.SDK(token_mp)

# 2. FUNÇÃO PARA GERAR A PREFERÊNCIA DE PAGAMENTO
def criar_link_pagamento(valor_venda):
    """Cria a preferência no Mercado Pago com retorno dinâmico para Codespaces/Produção."""
    email_cliente = st.session_state.usuario.get("email", "cliente@museia.com")
    # Captura o UUID do cliente para vincular à transação
    uuid_usuario = str(st.session_state.usuario.get('id'))
    
    # DETECÇÃO DINÂMICA DE URL: Resolve o problema do retorno no Codespaces
    try:
        # Tenta pegar a URL real onde o app está rodando agora
        host_header = st.context.headers.get("host")
        if host_header:
            host_atual = f"https://{host_header}"
        else:
            host_atual = "https://museia.streamlit.app"
    except:
        host_atual = "https://museia.streamlit.app"
    
    preference_data = {
        "items": [
            {
                "title": f"{NOME_PLANO} - Acesso à Central MuseIA por {DIAS_ACESSO} dias",
                "quantity": 1,
                "unit_price": valor_venda,
                "currency_id": "BRL"
            }
        ],
        "payer": {
            "email": email_cliente
        },
        # Vínculo essencial para seu banco de dados
        "external_reference": uuid_usuario,
        "back_urls": {
            "success": f"{host_atual}/pagamento?status=approved",
            "failure": f"{host_atual}/pagamento?status=failure",
            "pending": f"{host_atual}/pagamento?status=pending"
        },
        "auto_return": "approved",
       "payment_methods": {
            # Aqui dizemos ao Mercado Pago para BLOQUEAR tudo que não for Pix
            "excluded_payment_types": [
                {"id": "credit_card"},
                {"id": "debit_card"},
                {"id": "ticket"},
                {"id": "atm"}
            ],
            "installments": 1 
        }
    }
    
    result = sdk.preference().create(preference_data)
    return result["response"]["init_point"]

# =========================
# 🎬 HERO / DESTAQUE
# =========================
st.markdown("## 💡 Resolver o que eu preciso")

st.caption("Sem complicação. Comece agora.")

st.divider()

# =========================
# 💳 CARD PRINCIPAL (CENTRALIZADO)
# =========================
col1, col2, = st.columns([2, 2])

with col2:
    st.markdown("### 🔓 Acesso completo MuseIA")

    st.metric(
        label=f"{DIAS_ACESSO} dias de acesso",
        value=f"R$ {PRECO_ACESSO:.2f}",
        delta=f"De R$ {PRECO_REFERENCIA:.2f}"
    )

    st.caption("✔ Acesso imediato • ✔ Sem assinatura")

    st.divider()

    st.markdown("#### 🎁 O que você desbloqueia")

    st.markdown("""
- 🤖 Use seu agente quantas vezes quiser  
- 🧠 Experimente outros agentes da MuseIA  
- 📄 Crie e melhore seus conteúdos  
- ⚡ Resolva tarefas do dia a dia mais rápido   
""")

    st.divider()

# =========================
# 🎯 PROVA / CONTEXTO
# =========================
st.info("💡 Você paga uma vez e usa. Sem assinatura.")

# =========================
# 🔐 CHECKOUT
# =========================
if not st.session_state.get("logado"):
    st.warning("Entre ou crie sua conta para começar")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("👉 Entrar para começar", use_container_width=True):
            st.switch_page("pages/login.py")

else:
    nome = st.session_state.usuario.get("nome")

    st.success(f"{nome}, você já pode começar 👇")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(f"💳 Começar agora por R$ {PRECO_ACESSO:.2f}", use_container_width=True):
            try:
                with st.spinner("Gerando pagamento..."):
                    link_mp = criar_link_pagamento(PRECO_ACESSO)

                st.markdown(f"[👉 Clique aqui para pagar]({link_mp})")
                st.info("💡 Pix libera em segundos")

            except Exception as e:
                st.error(f"Erro ao gerar pagamento: {e}")


# 5. PROCESSAMENTO DO RETORNO (Ativação Automática)
if st.query_params.get("status") == "approved":
    try:
        supabase = get_client()
        user_uuid = st.session_state.usuario['id']
        
        # Calcula a data de vencimento (Hoje + 30 dias)
        data_vencimento = (datetime.now() + timedelta(days=DIAS_ACESSO)).strftime('%Y-%m-%d')
        
        with st.spinner("Ativando sua conta..."):
            # Atualiza o status e o vencimento no Supabase
            supabase.table("usuarios").update({
                "status_pagamento": "ativo", 
                "venc": data_vencimento
            }).eq("id", user_uuid).execute()
        
        # Atualiza a sessão para o usuário não precisar logar de novo
        st.session_state.usuario["status_pagamento"] = "ativo"
        st.session_state.usuario["venc"] = data_vencimento
        
        st.balloons()
        st.success("✨ Tudo pronto! Você já pode usar seu agente.")
        
        time.sleep(3)
        st.switch_page("pages/agentes.py")
        
    except Exception as e:
        st.error(f"Erro ao atualizar acesso no banco: {e}")
        # No arquivo pages/login.py
st.markdown("---")
if st.button("Escolha seu Agente"):
    # Chamando o arquivo da vitrine diretamente
    st.switch_page("pages/agentes.py")
