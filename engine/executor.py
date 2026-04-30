from engine.input_handler import tratar_input
from engine.ai_handler import executar_ia
from engine.processadores import executar_logica_python


def executar_agente(agente, input_data, contexto_extra=None):
    """
    Motor de execução da MuseIA.
    agente: dicionário vindo do Supabase.
    input_data: conteúdo bruto (texto, PDF, CSV etc).
    contexto_extra: contexto adicional do usuário.
    """

    # =========================================================
    # 1. PARÂMETROS DO AGENTE
    # =========================================================
    tipo = agente.get("tipo_input", "texto")
    prompt_mestre = agente.get("prompt_base", "")
    id_robo = agente.get("id_robo", None)

    # =========================================================
    # 2. TRATAMENTO DE ENTRADA
    # =========================================================
    try:
        dados_processados = tratar_input(input_data, tipo)
    except Exception as e:
        return f"Erro ao processar sua entrada: {str(e)}"

    # =========================================================
    # 3. EXECUÇÃO DAS REGRAS (ROBÔS PYTHON PURO)
    # =========================================================
    try:
        resultado_regras = executar_logica_python(
            id_robo,
            dados_processados,
            contexto_extra
        )
    except Exception as e:
        resultado_regras = f"Erro nas regras do robô: {str(e)}"

    # =========================================================
    # 4. CONSTRUÇÃO DO PROMPT FINAL (IA GENERATIVA)
    # =========================================================
    prompt_final = f"""
{prompt_mestre}

===============================
📌 RESULTADO DAS REGRAS
===============================
{resultado_regras}

===============================
📌 CONTEXTO DO USUÁRIO
===============================
{contexto_extra if contexto_extra else "Nenhum contexto adicional"}
"""

    # =========================================================
    # 5. EXECUÇÃO DA IA
    # =========================================================
    try:
        resultado_ia = executar_ia(prompt_final, dados_processados)
        return resultado_ia

    except Exception as e:
        return f"Erro na comunicação com a IA: {str(e)}"
