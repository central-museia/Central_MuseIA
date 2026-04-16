import requests
from bs4 import BeautifulSoup


# =========================================
# 🌐 BUSCAR HTML DA PÁGINA
# =========================================
def obter_html(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        return response.text

    except:
        return None


# =========================================
# 🧠 EXTRAIR TEXTO LIMPO
# =========================================
def extrair_texto(url):

    html = obter_html(url)

    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    # remove scripts e estilos
    for tag in soup(["script", "style"]):
        tag.decompose()

    texto = soup.get_text(separator=" ")

    # limpa espaços
    texto = " ".join(texto.split())

    return texto


# =========================================
# 🎯 EXTRAIR TÍTULO DA PÁGINA
# =========================================
def extrair_titulo(url):

    html = obter_html(url)

    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    if soup.title:
        return soup.title.string

    return ""


# =========================================
# 📉 TEXTO LIMITADO (PARA IA)
# =========================================
def extrair_texto_resumido(url, limite=3000):

    texto = extrair_texto(url)

    return texto[:limite]
