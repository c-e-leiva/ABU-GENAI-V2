# resumen_historial.py
# Módulo encargado de generar un resumen de la conversación entre el usuario y ABU,
# utilizando el historial almacenado en memoria y un modelo de lenguaje (GPT) para procesarlo.

from core.memoria import obtener_historial_resumen

# 🧠 Función principal que genera un resumen de la conversación con ABU
# Utiliza el historial de mensajes guardado y el modelo GPT-3.5-turbo para generar un texto afectuoso y sintético.
def generar_resumen(client):
    historial = obtener_historial_resumen()

    # Verifica que haya suficiente historial para generar un resumen
    if not historial.strip() or len(historial.split("\n")) < 2:
        return "Todavía no hay suficiente historial para generar un resumen."

    # Construye el prompt con instrucciones para resumir la conversación de forma cálida y humana
    prompt = (
        "A continuación verás el historial de conversación entre una persona mayor y ABU, un asistente virtual empático diseñado para acompañarla emocionalmente. "
        "Tu tarea es generar un resumen claro, humano y breve de lo que se habló, aclarando que fue una conversación entre el usuario y el asistente ABU. "
        "Incluí emociones, temas tratados, intereses personales mencionados por la persona mayor y el tono general de la charla. "
        "Hace un listado de las emociones detectadas por la persona mayor. "
        "El resumen debe tener un lenguaje afectuoso pero claro y no debe inventar información.\n\n"
        f"{historial}"
    )

    # Envia el prompt al modelo GPT-3.5-turbo mediante la API de OpenAI (pasada como `client`)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sos un asistente que resume conversaciones con personas mayores."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=400,
    )

    # Devuelve el texto generado como resumen final
    return response.choices[0].message.content.strip()
