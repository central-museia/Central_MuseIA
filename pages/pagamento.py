import streamlit as st
import mercadopago
import os
import time
from datetime import datetime, timedelta
from database.cliente import get_client

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

# 3. INTERFACE VISUAL
st.title("💳 Ative seu Acesso Premium")

# Banner de Ancoragem de Preço
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #0f0f0f, #1c1c1c);
    padding: 30px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(229,9,20,0.3);
    margin-bottom: 30px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
">

    <p style="
        color: #e50914;
        font-weight: bold;
        letter-spacing: 1px;
        font-size: 13px;
        margin-bottom: 10px;
    ">
        PASSE MUSEIA
    </p>

    <h2 style="
        color: white;
        font-size: 42px;
        margin: 0;
        font-weight: 700;
    ">
        R$ {PRECO_ACESSO:.2f}
    </h2>

    <p style="
        color: #bbb;
        font-size: 14px;
        margin-top: 5px;
        text-decoration: line-through;
    ">
        De R$ {PRECO_REFERENCIA:.2f}
    </p>

    <p style="
        color: #00ff9c;
        font-weight: 600;
        margin-top: 12px;
        font-size: 16px;
    ">
        Acesso por {DIAS_ACESSO} dias
    </p>

    <div style="
        margin-top: 18px;
        padding: 15px;
        background-color: rgba(255,255,255,0.03);
        border-radius: 10px;
    ">
        <p style="color: #ddd; margin: 0; font-size: 14px;">
            Use seu agente e explore outros agentes da Central MuseIA durante o período
        </p>
    </div>

    <p style="
        color: #888;
        font-size: 12px;
        margin-top: 15px;
    ">
        Sem assinatura • Ativação imediata
    </p>

</div>
""", unsafe_allow_html=True)

# 4. LÓGICA DE CHECKOUT
if not st.session_state.get("logado"):
    st.warning("Acesse sua conta para liberar o checkout.")
    if st.button("Fazer Login ou Cadastro", use_container_width=True):
        st.switch_page("pages/login.py")
else:
    st.write(f"""
Olá, **{st.session_state.usuario.get('nome')}** 👋  

Ative seu acesso agora e utilize seu agente com inteligência artificial.  
Você também terá acesso à Central MuseIA por {DIAS_ACESSO} dias para explorar outras soluções.
""")
    
    if st.button("Gerar Pagamento Seguro (Pix ou Cartão)", use_container_width=True):
        try:
            with st.spinner("Conectando ao Mercado Pago..."):
                link_mp = criar_link_pagamento(PRECO_ACESSO)
                
                st.success("Tudo pronto! Pague agora para ativar seu acesso:")
                st.markdown(f'''
                    <a href="{link_mp}" target="_blank">
                        <button style="width:100%; height:60px; background-color:#009ee3; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold; font-size:20px; box-shadow: 0 4px 15px rgba(0,158,227,0.3);">
                            Ativar acesso por R$ {PRECO_ACESSO:.2f}
                        </button>
                    </a>
                ''', unsafe_allow_html=True)
                st.info("💡 Dica: O Pix libera seu acesso em segundos!")
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
        st.success("✨ Pagamento Confirmado! Seu acesso está liberado.")
        
        time.sleep(3)
        st.switch_page("pages/agentes.py")
        
    except Exception as e:
        st.error(f"Erro ao atualizar acesso no banco: {e}")
        # No arquivo pages/login.py
st.markdown("---")
if st.button("Escolha seu Agente"):
    # Chamando o arquivo da vitrine diretamente
    st.switch_page("pages/agentes.py")
