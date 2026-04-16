from engine.input_handler import tratar_input
from engine.ai_handler import executar_ia
from engine.processadores import executar_logica_python

def executar_agente(agente, input_data, contexto_extra=None):
    """
    Motor de execução da MuseIA.
    agente: dicionário com os dados do robô vindos do Supabase.
    input_data: conteúdo bruto (texto, arquivo, etc).
    contexto_extra: informações adicionais como 'cargo desejado'.
    """

    # 1. RECUPERAÇÃO DE PARÂMETROS
    # Usamos .get() com valores padrão para o código não quebrar se a coluna estiver vazia
    tipo = agente.get("tipo_input", "texto") 
    prompt_mestre = agente.get("prompt_base", "")

    # 2. TRATAMENTO DE ENTRADA (Limpando o que o usuário enviou)
    try:
        dados_processados = tratar_input(input_data, tipo)
    except Exception as e:
        return f"Erro ao processar sua entrada: {str(e)}"

    # 3. CONSTRUÇÃO DO PROMPT FINAL
    # Combinamos a inteligência do agente + o contexto do cliente
    if contexto_extra:
        prompt_final = f"{prompt_mestre}\n\nCONTEXTO ADICIONAL:\n{contexto_extra}"
    else:
        prompt_final = prompt_mestre

    # 4. EXECUÇÃO DA INTELIGÊNCIA ARTIFICIAL
    try:
        resultado = executar_ia(prompt_final, dados_processados)
        return resultado
    except Exception as e:
        return f"Erro na comunicação com a IA: {str(e)}"