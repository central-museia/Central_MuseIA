from database.cliente import get_client
import streamlit as st

# =========================================
# 🖼️ STORAGE - ASSETS PRIVADOS
# =========================================

@st.cache_data(ttl=3600)
def get_asset_url(file_name):
    try:
        supabase = get_client()

        response = supabase.storage.from_("assets").create_signed_url(
            file_name, 3600
        )

        return response.get("signedURL")

    except Exception as e:
        print(f"Erro ao gerar URL do asset: {str(e)}")
        return None