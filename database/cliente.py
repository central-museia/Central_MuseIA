from supabase import create_client
import streamlit as st
import bcrypt
from datetime import datetime

# =========================================
# 🔌 CONEXÃO SUPABASE
# =========================================
def get_client():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["anon_key"]
        return create_client(url, key)
    except Exception:
        st.error("Erro de Configuração: Chaves do Supabase não encontradas.")
        st.stop()

# =========================================
# 🔐 SEGURANÇA
# =========================================
def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha_digitada, senha_hash):
    return bcrypt.checkpw(senha_digitada.encode(), senha_hash.encode())

# =========================================
# 🚀 OPERAÇÕES
# =========================================

def cadastrar_usuario(nome, email, senha):
    try:
        supabase = get_client()
        email_limpo = email.strip().lower()

        # 1. VERIFICAÇÃO (Já existe no seu código)
        checar = supabase.table("usuarios").select("email").eq("email", email_limpo).execute()
        if checar.data:
            return False, "Este e-mail já está cadastrado na MuseIA."

        # 3. SALVAR NA SUA TABELA (O que você já faz)
        senha_protegida = hash_senha(senha)
        dados = {
            "nome": nome,
            "email": email_limpo,
            "senha": senha_protegida,
            "status_pagamento": "pendente"
        }
        supabase.table("usuarios").insert(dados).execute()
        return True, "Cadastro realizado!"
    except Exception as e:
        return False, f"Erro: {str(e)}"

# Mantenha as funções de validar_login e recuperar_senha abaixo...
# =========================================
# 🔐 ACESSO
# =========================================

def validar_login(email, senha):
    """
    Verifica se o usuário existe e se a senha bate com o hash.
    Retorna o dicionário do usuário se OK, ou None se falhar.
    """
    try:
        supabase = get_client()
        email_limpo = email.strip().lower()

        # Busca o usuário pelo e-mail
        response = supabase.table("usuarios").select("*").eq("email", email_limpo).execute()

        if response.data:
            usuario = response.data[0]
            
            # 1. Verifica se está bloqueado (Segurança MuseIA)
            if usuario.get("bloqueado"):
                st.error("Conta bloqueada. Entre em contato com o suporte.")
                return None
            
            # 2. Verifica a senha usando Bcrypt
            senha_hash = usuario.get("senha")
            if senha_hash and verificar_senha(senha, senha_hash):
                return usuario
        
        return None
    except Exception as e:
        st.error(f"Erro ao conectar com o banco: {e}")
        return None

def recuperar_senha(email):
    try:
        supabase = get_client()
        email_limpo = email.strip().lower()
        
        # 1. Verifica na nossa base de dados oficial
        res = supabase.table("usuarios").select("email").eq("email", email_limpo).execute()
        
        if res.data:
            # 2. Aciona o motor do Supabase com o template que você editou
            # O link de redirecionamento agora é automático via painel
            supabase.auth.reset_password_for_email(email_limpo)
            
            return True, "Sinal enviado! Verifique seu e-mail para definir uma nova senha na MuseIA."
        
        return False, "Este e-mail não consta em nossa base de assinantes."
        
    except Exception as e:
        # Tratamento de limite de disparos para evitar bloqueios
        if "rate limit" in str(e).lower():
            return False, "Muitas solicitações seguidas. Aguarde um momento e tente novamente."
        return False, "O sistema de e-mail está em manutenção. Tente novamente mais tarde."        
# =========================================
# 🔐 CATÁLOGO
# =========================================

def obter_agentes():
    """Traz todos os dados dos robôs (nome, imagem, links)"""
    try:
        supabase = get_client()
        # Buscamos apenas os ativos para garantir que o cliente só veja o que está pronto
        res = supabase.table("agentes").select("*").eq("ativo", True).execute()
        return res.data if res.data else []
    except Exception as e:
        st.error(f"Erro ao carregar catálogo: {e}")
        return []

def obter_perfis():
    """Busca as categorias de perfis para os filtros do site"""
    try:
        supabase = get_client()
        # Traz os nomes dos perfis que você marcou como ativos no banco
        res = supabase.table("perfis").select("nome").eq("ativo", True).execute()
        return [item['nome'] for item in res.data]
    except Exception:
        return []

def obter_colecoes():
    """Busca as coleções (packs) disponíveis"""
    try:
        supabase = get_client()
        res = supabase.table("colecoes").select("nome").eq("ativo", True).execute()
        return [item['nome'] for item in res.data]
    except Exception:
        return []
