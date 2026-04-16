def executar_logica_python(id_robo, dados, contexto_extra=None):
    """
    Aqui moram os seus robôs de Python Puro.
    """
    
    if id_robo == "formatador_wfm":
        # Exemplo: Um robô que apenas limpa espaços e coloca em maiúsculo
        return dados.strip().upper()

    if id_robo == "calculadora_escala":
        # Sua lógica matemática de WFM aqui
        return "Resultado do cálculo de escala..."

    return f"Robô Python '{id_robo}' ainda não tem lógica definida."