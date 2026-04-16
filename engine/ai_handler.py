from gemini import gemini

client = gemini()

def executar_ia(prompt, dados):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # custo baixo e rápido
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": str(dados)
                }
            ],
            temperature=0.3  # mais consistente, menos aleatório
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Erro na IA: {str(e)}"