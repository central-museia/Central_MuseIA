import pandas as pd

def tratar_input(input_data, tipo):

    if tipo == "texto":
        return input_data

    elif tipo == "csv":
        try:
            df = pd.read_csv(input_data)
            return df.to_string()
        except Exception as e:
            return f"Erro ao ler CSV: {e}"

    elif tipo == "pdf":
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(input_data)
            texto = ""

            for page in reader.pages:
                texto += page.extract_text() or ""

            return texto

        except Exception as e:
            return f"Erro ao ler PDF: {e}"

    # fallback
    return str(input_data)