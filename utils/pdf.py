import pdfplumber
from fpdf import FPDF
import re
import pandas as pd

# =========================================
# 📄 LEITURA (Insumo Bruto)
# =========================================
def ler_pdf_completo(arquivo):
    """Lê o PDF do cliente integralmente. O descarte do que não interessa 
    será feito pela lógica do Agente, não aqui."""
    texto_bruto = ""
    try:
        with pdfplumber.open(arquivo) as pdf:
            for pagina in pdf.pages:
                conteudo = pagina.extract_text()
                if conteudo: 
                    texto_bruto += conteudo + "\n"
        return texto_bruto
    except Exception as e:
        return f"Erro na leitura: {e}"


# =========================================
# 📄 LEITURA UNIVERSAL (PDF, CSV, TXT)
# =========================================
def ler_arquivo(arquivo):
    """Identifica o tipo do arquivo e realiza a leitura adequada."""
    try:
        tipo = arquivo.type

        # PDF
        if tipo == "application/pdf":
            return ler_pdf_completo(arquivo)

        # CSV
        elif tipo == "text/csv":
            df = pd.read_csv(arquivo)
            return df.to_string()

        # TXT
        elif tipo == "text/plain":
            return arquivo.read().decode("utf-8")

        return "Formato de arquivo não suportado."

    except Exception as e:
        return f"Erro na leitura: {e}"


# =========================================
# 📄 ESCRITA (Entrega Blindada do Produto)
# =========================================
def exportar_resultado_pdf(texto_resultado, agente_nome):
    """Gera o PDF garantindo que nenhum caractere especial (como travessões) 
    trave a entrega. O que não for compatível com Helvetica é descartado."""
    
    # Filtro Radical: Mantém apenas letras, números e pontuação básica (ASCII)
    texto_seguro = re.sub(r'[^\x20-\x7E\n]', '', str(texto_resultado))
    nome_seguro = re.sub(r'[^\x20-\x7E\n]', '', str(agente_nome))

    pdf = FPDF()
    pdf.add_page()
    
    # Identidade MuseIA
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(229, 9, 20) 
    pdf.cell(0, 10, "MUSEIA DIGITAL", ln=True, align='L')
    pdf.line(10, 20, 200, 20)
    pdf.ln(10)
    
    # Título do Relatório
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, f"Relatorio: {nome_seguro}", ln=True)
    pdf.ln(5)
    
    # Corpo (Texto processado e limpo)
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, texto_seguro)
    
    return bytes(pdf.output(dest='S'))