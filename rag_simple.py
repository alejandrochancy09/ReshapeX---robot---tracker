"""
Sistema RAG simple para consultar el estado de despliegue de robots de ReshapeX.

Flujo:
    1. Retrieval: busca en la base de conocimiento los registros relevantes.
    2. Augmentation: arma un prompt con la pregunta y esos registros.
    3. Generation: Claude responde usando solo esos datos.
"""

import os
import sys

import anthropic
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

load_dotenv()  # carga las variables definidas en el archivo .env

MODELO = "claude-haiku-4-5"
MAX_TOKENS = 1024

SYSTEM_PROMPT = (
    "Eres un asistente experto en despliegue de robots industriales para ReshapeX. "
    "Responde de forma clara y concisa, basándote solo en los datos que te entregan. "
    "Si los datos no alcanzan para responder, dilo explícitamente. "
    "Responde en texto plano, sin Markdown: no uses asteriscos, tablas ni encabezados."
)

BASE_DE_CONOCIMIENTO = [
    {"id": "RBT-0041", "tipo": "Welding Unit",    "status": "deployed",   "progreso": 100, "cliente": "Volcarex Auto"},
    {"id": "RBT-0078", "tipo": "Precision Drill", "status": "deployed",   "progreso": 100, "cliente": "Nexford Steel"},
    {"id": "RBT-0055", "tipo": "Coating Robot",   "status": "inprogress", "progreso": 63,  "cliente": "Lumex Corp"},
    {"id": "RBT-0072", "tipo": "Inspection Unit", "status": "inprogress", "progreso": 45,  "cliente": "Volcarex Auto"},
    {"id": "RBT-0089", "tipo": "Welding Unit",    "status": "pending",    "progreso": 0,   "cliente": "Nexford Steel"},
]


# ---------------------------------------------------------------------------
# Cliente de la API
# ---------------------------------------------------------------------------

def crear_cliente() -> anthropic.Anthropic:
    """Crea el cliente de Anthropic usando la API key del archivo .env."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Error: no se encontró ANTHROPIC_API_KEY. Revisa el archivo .env.")
    return anthropic.Anthropic(api_key=api_key)


# ---------------------------------------------------------------------------
# Paso 1: Retrieval
# ---------------------------------------------------------------------------

def buscar(pregunta: str, base: list[dict]) -> list[dict]:
    """
    Devuelve los robots de la base que son relevantes para la pregunta.

    Primero filtra por cliente (si la pregunta menciona alguno) y después
    por estado. Así se pueden combinar, por ejemplo:
    "robots desplegados de Volcarex Auto".
    """
    pregunta = pregunta.lower()
    resultados = base

    # Filtro 1: cliente mencionado en la pregunta
    clientes_mencionados = {r["cliente"] for r in base if r["cliente"].lower() in pregunta}
    if clientes_mencionados:
        resultados = [r for r in resultados if r["cliente"] in clientes_mencionados]

    # Filtro 2: estado o progreso
    if "mantenimiento" in pregunta or "progreso" in pregunta:
        resultados = [r for r in resultados if r["progreso"] < 100]
    elif "desplegado" in pregunta or "deployed" in pregunta:
        resultados = [r for r in resultados if r["status"] == "deployed"]
    elif "pendiente" in pregunta:
        resultados = [r for r in resultados if r["status"] == "pending"]
    elif not clientes_mencionados:
        # No se reconoció ni un cliente ni un estado
        resultados = []

    return resultados


# ---------------------------------------------------------------------------
# Paso 2: Augmentation
# ---------------------------------------------------------------------------

def enriquecer_prompt(pregunta: str, registros: list[dict]) -> str:
    """Arma el mensaje para Claude con la pregunta y los registros encontrados."""
    if registros:
        lineas = [
            f"- {r['id']} ({r['tipo']}) — {r['cliente']} — {r['status']} — {r['progreso']}%"
            for r in registros
        ]
        contexto = "\n".join(lineas)
    else:
        contexto = "(No se encontraron registros relevantes.)"

    return (
        f"Pregunta del usuario: {pregunta}\n\n"
        f"Datos relevantes de la base de conocimiento:\n{contexto}"
    )


# ---------------------------------------------------------------------------
# Paso 3: Generation
# ---------------------------------------------------------------------------

def generar_respuesta(cliente: anthropic.Anthropic, prompt: str) -> str:
    """Envía el prompt a Claude y devuelve el texto de la respuesta."""
    try:
        respuesta = cliente.messages.create(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIConnectionError:
        return "Error: no se pudo conectar con la API. Revisa tu conexión a internet."
    except anthropic.RateLimitError:
        return "Error: se superó el límite de solicitudes. Espera un momento e intenta de nuevo."
    except anthropic.APIStatusError as error:
        return f"Error de la API (código {error.status_code}): {error.message}"

    return respuesta.content[0].text


# ---------------------------------------------------------------------------
# Sistema RAG completo
# ---------------------------------------------------------------------------

def preguntar(cliente: anthropic.Anthropic, pregunta: str) -> str:
    """Ejecuta los tres pasos del RAG y devuelve la respuesta de Claude."""
    print(f"\nPregunta: {pregunta}")
    print("-" * 50)

    registros = buscar(pregunta, BASE_DE_CONOCIMIENTO)
    print(f"Retrieval: {len(registros)} registros encontrados")

    prompt = enriquecer_prompt(pregunta, registros)
    print("Augmentation: prompt enriquecido")

    respuesta = generar_respuesta(cliente, prompt)
    print("Generation: respuesta de Claude\n")

    return respuesta


def main() -> None:
    """Corre unas preguntas de prueba."""
    cliente = crear_cliente()

    preguntas_de_prueba = [
        "¿Cuáles robots necesitan mantenimiento?",
        "¿Qué robots tiene Volcarex Auto?",
        "¿Cuántos robots están desplegados?",
        "¿Qué robots desplegados tiene Volcarex Auto?",
    ]

    for pregunta in preguntas_de_prueba:
        respuesta = preguntar(cliente, pregunta)
        print(f"Respuesta: {respuesta}")


if __name__ == "__main__":
    main()
