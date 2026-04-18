import pdfplumber
import pandas as pd
import re
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

# =========================================
# 📄 LEITURA (Insumo Bruto)
# =========================================
def ler_pdf_completo(arquivo):
    """Lê o PDF do cliente integralmente sem perdas."""
    texto_bruto = ""
    try:
        with pdfplumber.open(arquivo) as pdf:
            for pagina in pdf.pages:
                conteudo = pagina.extract_text()
                if conteudo: 
                    texto_bruto += conteudo + "\n"
        return texto_bruto
    except Exception as e:
        return f"Erro na leitura do PDF: {e}"

def ler_arquivo(arquivo):
    """Identifica o tipo do arquivo e realiza a leitura adequada."""
    try:
        nome_arquivo = arquivo.name.lower()

        if nome_arquivo.endswith('.pdf'):
            return ler_pdf_completo(arquivo)

        elif nome_arquivo.endswith('.csv'):
            df = pd.read_csv(arquivo)
            return df.to_string()

        elif nome_arquivo.endswith('.txt'):
            return arquivo.read().decode("utf-8")

        return "Formato de arquivo não suportado."
    except Exception as e:
        return f"Erro na leitura: {e}"

# =========================================
# 📄 ESCRITA (Entrega Premium MuseIA Digital)
# =========================================
def exportar_resultado_pdf(texto_resultado, agente_nome):
    """
    Gera o PDF com padrão visual MuseIA.
    Suporta acentuação completa via fonte DejaVuSans.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    # 1. Carregar Fonte (Adeus erro de acentuação!)
    try:
        # Certifique-se que o arquivo .ttf está na pasta fonts/
        pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))
        fonte_principal = 'DejaVu'
    except:
        fonte_principal = 'Helvetica' # Fallback se a fonte falhar

    # 2. Cabeçalho Visual MuseIA (Assinatura da Marca)
    c.setFillColorRGB(0.02, 0.05, 0.1) # Fundo Escuro Profissional
    c.rect(0, altura - 80, largura, 80, fill=1, stroke=0)
    
    c.setFillColor(colors.hexColor("#00FFCC")) # Verde Neon MuseIA
    c.setFont(fonte_principal, 18)
    c.drawString(40, altura - 45, "MUSEIA DIGITAL")
    
    c.setFillColor(colors.white)
    c.setFont(fonte_principal, 9)
    c.drawString(40, altura - 62, f"RELATÓRIO: {agente_nome.upper()}")
    c.drawRightString(largura - 40, altura - 62, f"GERADO EM: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # 3. Corpo do Texto (Processamento de Linhas)
    y = altura - 110
    c.setFillColor(colors.black)
    c.setFont(fonte_principal, 10)
    
    # Dividir o texto em linhas respeitando as quebras originais
    linhas = str(texto_resultado).split('\n')
    
    for linha in linhas:
        # Se a linha for muito longa, poderíamos quebrar, mas aqui 
        # mantemos a simplicidade para relatórios estruturados
        if y < 60: # Nova página automática
            c.showPage()
            y = altura - 50
            c.setFont(fonte_principal, 10)

        c.drawString(40, y, linha)
        y -= 14 # Espaçamento entre linhas

    # 4. Rodapé Fixo
    c.setFont(fonte_principal, 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(largura/2, 30, "Inteligência Humana que Controla a IA. | www.museiadigital.com.br")

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
