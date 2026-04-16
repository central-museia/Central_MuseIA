import streamlit as st
import google.generativeai as genai


# =========================================
# 🔧 CONFIGURAÇÃO
# =========================================
def configurar_ia():
    try:
        genai.configure(api_key=st.secrets["ia"]["gemini_key"])
    except Exception:
        raise Exception("Chave da IA não configurada corretamente.")


# =========================================
# 🧠 EXECUTOR PADRÃO DE IA
# =========================================
def executar_ia(prompt, modelo="gemini-1.5-flash"):

    try:
        configurar_ia()

        model = genai.GenerativeModel(modelo)

        response = model.generate_content(prompt)

        texto = response.text if response.text else ""

        # 🔒 Garantia mínima de resposta
        if not texto.strip():
            return "⚠️ A IA não retornou conteúdo válido."

        return texto

    except Exception as e:
        return f"⚠️ Erro ao executar IA: {str(e)}"


# =========================================
# 🎯 CONSTRUTOR DE PROMPT (PADRÃO MUSEIA)
# =========================================
def montar_prompt(texto, regras):

    objetivo = regras.get("objetivo", "Analise e responda de forma clara")
    tom = regras.get("tom", "profissional")
    formato = regras.get("formato", "texto simples")

    prompt = f"""
Você é um especialista em resolver problemas reais.

Objetivo:
{objetivo}

Tom da resposta:
{tom}

Formato esperado:
{formato}

Entrada:
{texto}

Responda de forma direta, prática e sem enrolação.
"""

    return prompt