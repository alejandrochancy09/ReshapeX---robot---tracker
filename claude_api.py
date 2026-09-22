import anthropic

API_KEY = "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"

cliente = anthropic.Anthropic(api_key=API_KEY)

respuesta = cliente.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "¿Qué es un robot Tool Changer en una línea?"}
    ]
)

print(f"Claude dice: {respuesta.content[0].text}")
