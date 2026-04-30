from engine.input_handler import tratar_input
from engine.ai_handler import executar_ia
from engine.processadores import executar_logica_python
from engine.prompt_loader import buscar_prompt_ativo


def executar_agente(agente, input_data, supabase, contexto_extra=None):

    # =========================================================
    # 1. DADOS DO AGENTE
    # =========================================================
    agente_id = agente["id"]
    codigo_python = agente.get("codigo_python", None)
    regras = agente.get("regras_processamento", {})

    # =========================================================
    # 2. PROMPT (BANCO DE DADOS)
    # =========================================================
    try:
        prompt_mestre = buscar_prompt_ativo(supabase, agente_id)
    except Exception as e:
        return f"Erro ao buscar prompt: {str(e)}"

    # =========================================================
    # 3. INPUT
    # =========================================================
    try:
        dados = tratar_input(input_data, "texto")
    except Exception as e:
        return f"Erro input: {str(e)}"

    # =========================================================
    # 4. ROBÔ (PYTHON PURO)
    # =========================================================
    resultado_robo = None

    if codigo_python:
        try:
            resultado_robo = executar_logica_python(
                agente_id,
                dados,
                contexto_extra
            )
        except Exception as e:
            resultado_robo = f"Erro robô: {str(e)}"

    # =========================================================
    # 5. PROMPT FINAL (IA GENERATIVA)
    # =========================================================
    prompt_final = f"""
{prompt_mestre}

========================
📌 REGRAS DO AGENTE
========================
{regras}

========================
📌 RESULTADO DO ROBÔ PYTHON
========================
{resultado_robo}

========================
📌 CONTEXTO DO USUÁRIO
========================
{contexto_extra if contexto_extra else "N/A"}

========================
📌 DADOS PROCESSADOS
========================
{dados}
"""

    # =========================================================
    # 6. IA COM FALLBACK
    # =========================================================
    try:
        resultado = executar_ia(
            prompt_final,
            dados,
            codigo_python
        )
        return resultado

    except Exception as e:
        return f"Erro na IA: {str(e)}"
