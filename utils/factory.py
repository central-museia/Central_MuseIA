def executar_agente(texto, regras, codigo_python=None):
    # O objeto agente_selecionado já deve vir com o prompt_texto 
    # carregado via JOIN no Supabase (agentes.id = prompts.agente_id)
    agente_completo = st.session_state.get("agente_selecionado", {})
    
    if not regras and not codigo_python:
        return texto

    if codigo_python:
        try:
            # Configuração enviada para o Chassi respeitando as tabelas
            config_envio = {
                "id": agente_completo.get("id"),
                "nome": agente_completo.get("nome"), # Usado apenas para o título do PDF
                "regras_processamento": agente_completo.get("regras_processamento", {}),
                "prompt": agente_completo.get("prompt_texto", "") # Texto da tabela prompts
            }

            escopo = {}
            exec(codigo_python, escopo)

            if "executar" in escopo:
                return escopo["executar"](texto, config_envio)

            return "⚠️ Função 'executar' não encontrada."
        except Exception as e:
            return f"⚠️ Erro: {str(e)}"
    
    # ... motores padrão ...
