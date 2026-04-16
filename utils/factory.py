from utils.ia import executar_ia, montar_prompt
from utils.scraping import extrair_texto_resumido

# =========================================
# 🔹 MOTOR WEB
# =========================================
def motor_web(texto, regras):
    conteudo = extrair_texto_resumido(texto)

    if not conteudo:
        return "⚠️ Não foi possível extrair conteúdo da página."

    return conteudo


# =========================================
# 🔹 MOTOR TEXTO
# =========================================
def motor_texto(texto, regras):
    resultado = texto

    for acao in regras.get("acoes", []):
        tipo = acao.get("tipo")

        if tipo == "resumir":
            resultado = resultado[:200]

        elif tipo == "limpar":
            resultado = resultado.strip()

        elif tipo == "organizar":
            linhas = resultado.split("\n")
            resultado = "\n".join([l.strip() for l in linhas if l.strip()])

    return resultado


# =========================================
# 🔹 MOTOR DECISÃO
# =========================================
def motor_decisao(texto, regras):
    texto_lower = texto.lower()

    if "urgente" in texto_lower:
        return "Prioridade: ALTA"

    elif "atraso" in texto_lower:
        return "Prioridade: MÉDIA"

    return "Prioridade: NORMAL"


# =========================================
# 🔹 MOTOR ESTRUTURADO
# =========================================
def motor_estruturado(texto, regras):
    import re

    valores = re.findall(r'\d+,\d{2}', texto)
    valores = [float(v.replace(",", ".")) for v in valores]

    total = sum(valores)

    return f"Total identificado: R$ {total:.2f}"


# =========================================
# 🔥 ORQUESTRADOR PRINCIPAL
# =========================================
def executar_agente(texto, regras, codigo_python=None):

    if not regras and not codigo_python:
        return texto

    # 🔹 PRIORIDADE 1: CODIGO DO BANCO (COLUNA SEPARADA)
    if codigo_python:
        try:
            escopo = {}
            exec(codigo_python, escopo)

            if "executar" in escopo:
                return escopo["executar"](texto)

            return "⚠️ Função 'executar' não encontrada no código."

        except Exception as e:
            return f"⚠️ Erro ao executar código do agente: {str(e)}"

    # 🔹 PRIORIDADE 2: MOTOR PADRÃO
    motor_nome = regras.get("motor")
    usar_ia = regras.get("usar_ia", False)

    mapa_motores = {
        "texto": motor_texto,
        "decisao": motor_decisao,
        "estruturado": motor_estruturado,
        "web": motor_web,
    }

    motor = mapa_motores.get(motor_nome)

    if motor:
        resultado = motor(texto, regras)

        if resultado:
            return resultado

    # 🔹 PRIORIDADE 3: IA
    if usar_ia:
        prompt = montar_prompt(texto, regras)
        return executar_ia(prompt)

    return "⚠️ Não foi possível processar a solicitação."