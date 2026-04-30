from gemini import gemini

client = gemini()


def executar_ia(prompt, dados, fallback_codigo=None):

    modelos = [
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]

    erro_geral = None

    # =========================================================
    # 🧠 1. TENTA GEMINI (ROTEAMENTO INTELIGENTE)
    # =========================================================
    for modelo in modelos:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=f"""
{prompt}

====================
DADOS
====================
{dados}
"""
            )

            if response and response.text:
                return response.text

        except Exception as e:
            erro_geral = str(e)
            continue

    # =========================================================
    # ⚙️ 2. FALLBACK: CÓDIGO PYTHON (ROBÔ LOCAL)
    # =========================================================
    if fallback_codigo:
        try:
            local = {"dados": dados, "resultado": None}
            exec(fallback_codigo, {}, local)
            return local.get("resultado", "Sem retorno do robô Python")

        except Exception as e:
            return f"Falha no fallback Python: {str(e)}"

    # =========================================================
    # 🚨 3. FALLBACK FINAL (SE TUDO FALHAR)
    # =========================================================
    return f"Sem resposta da IA. Último erro: {erro_geral}"
