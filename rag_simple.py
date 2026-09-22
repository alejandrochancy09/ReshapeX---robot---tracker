import anthropic

# Configuración
API_KEY = "su-api-key-aquí"
cliente = anthropic.Anthropic(api_key=API_KEY)

# BASE DE CONOCIMIENTO
base_de_conocimiento = [
    {"id": "RBT-0041", "tipo": "Welding Unit",    "status": "deployed",   "progreso": 100, "cliente": "Volcarex Auto"},
    {"id": "RBT-0078", "tipo": "Precision Drill", "status": "deployed",   "progreso": 100, "cliente": "Nexford Steel"},
    {"id": "RBT-0055", "tipo": "Coating Robot",   "status": "inprogress", "progreso": 63,  "cliente": "Lumex Corp"},
    {"id": "RBT-0072", "tipo": "Inspection Unit", "status": "inprogress", "progreso": 45,  "cliente": "Volcarex Auto"},
    {"id": "RBT-0089", "tipo": "Welding Unit",    "status": "pending",    "progreso": 0,   "cliente": "Nexford Steel"},
]

# PASO 1 — RETRIEVAL
def buscar(pregunta):
    pregunta = pregunta.lower()
    resultados = []
    for robot in base_de_conocimiento:
        if "mantenimiento" in pregunta or "progreso" in pregunta:
            if robot["progreso"] < 100:
                resultados.append(robot)
        elif "desplegado" in pregunta or "deployed" in pregunta:
            if robot["status"] == "deployed":
                resultados.append(robot)
        elif "pendiente" in pregunta:
            if robot["status"] == "pending":
                resultados.append(robot)
        elif robot["cliente"].lower() in pregunta:
            resultados.append(robot)
    return resultados

# PASO 2 — AUGMENTATION
def enriquecer_prompt(pregunta, contexto):
    contexto_texto = ""
    for robot in contexto:
        contexto_texto += f"- {robot['id']} ({robot['tipo']}) — {robot['cliente']} — {robot['status']} — {robot['progreso']}%\n"
    return f"""Eres un asistente experto en despliegue de robots industriales para ReshapeX.
    
Pregunta del usuario: {pregunta}

Datos relevantes de la base de conocimiento:
{contexto_texto}

Responde de forma clara y concisa basándote solo en estos datos. Si no hay datos relevantes, dilo."""

# PASO 3 — GENERATION con Claude real
def generar_respuesta(prompt):
    respuesta = cliente.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.content[0].text

# SISTEMA RAG COMPLETO
def preguntar(pregunta):
    print(f"\nPregunta: {pregunta}")
    print("-" * 50)
    contexto = buscar(pregunta)
    print(f"Retrieval: {len(contexto)} registros encontrados")
    prompt = enriquecer_prompt(pregunta, contexto)
    print("Augmentation: prompt enriquecido")
    respuesta = generar_respuesta(prompt)
    print(f"Generation: respuesta de Claude\n")
    print(f"Respuesta: {respuesta}")

# PRUEBAS
preguntar("¿Cuáles robots necesitan mantenimiento?")
preguntar("¿Qué robots tiene Volcarex Auto?")
preguntar("¿Cuántos robots están desplegados?")