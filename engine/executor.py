from engine.input_handler import tratar_input
from engine.ai_handler import executar_ia
from engine.processadores import executar_logica_python
from engine.prompt_loader import buscar_prompt_ativo


def executar_agente(agente, input_data, supabase, contexto_extra=None):

    # =========================================================
    # 1. DADOS DO AGENTE (REAL)
    # =========================================================
    agente_id = agente["id"]
    codigo_python = agente.get("codigo_python", None)
    regras = agente.get("regras_processamento", {})

    # =========================================================
    # 2. PROMPT (TABELA PROMPTS)
    # =========================================================
    def buscar_prompt_ativo(supabase, agente_id):
    res = (
        supabase.table("prompts")
        .select("prompt")
        .eq("agente_id", agente_id)
        .eq("ativo", True)
        .single()
        .execute()
    )

    return res.data["prompt"] if res.data else ""

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
📌 ROBÔ PYTHON
========================
{resultado_robo}

========================
📌 CONTEXTO
========================
{contexto_extra if contexto_extra else "N/A"}
"""

    # =========================================================
    # 6. IA
    # =========================================================
    return executar_ia(prompt_final, dados)
