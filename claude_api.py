import anthropic

API_KEY = "API_KEY = "su-api-key-aquí""

cliente = anthropic.Anthropic(api_key=API_KEY)

respuesta = cliente.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "¿Qué es un robot Tool Changer en una línea?"}
    ]
)

print(f"Claude dice: {respuesta.content[0].text}")
