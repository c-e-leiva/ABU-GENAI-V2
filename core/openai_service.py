# openai_service.py
# Módulo para gestionar la conexión con la API de OpenAI y generar respuestas conversacionales.

import os
from openai import OpenAI


# --- Crear cliente de OpenAI ---
def crear_cliente(api_key: str = None) -> OpenAI:
    """
    Crea una instancia del cliente de OpenAI.

    Parámetros:
        api_key (str): Clave de API opcional. Si no se proporciona, intenta obtenerla desde las variables de entorno.

    Retorna:
        OpenAI: Cliente autenticado para realizar peticiones a la API.

    Lanza:
        ValueError: Si no se encuentra una clave de API válida.
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")  # Intenta obtener la API key desde el entorno
    if not api_key:
        raise ValueError(
            "No se encontró la API key de OpenAI. "
            "Asegurate de definir OPENAI_API_KEY en el archivo .streamlit/config.toml o en las variables de entorno."
        )
    return OpenAI(api_key=api_key)  # Devuelve una instancia del cliente


# --- Obtener respuesta desde el modelo GPT ---
def obtener_respuesta(client: OpenAI, messages: list) -> str:
    """
    Envía un historial de mensajes a la API de OpenAI y obtiene la respuesta generada.

    Parámetros:
        client (OpenAI): Cliente de OpenAI ya autenticado.
        messages (list): Lista de mensajes en formato [{"role": "user/assistant/system", "content": "texto"}].

    Retorna:
        str: Contenido textual de la respuesta del modelo (sin espacios al principio o final).
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",        # Se utiliza el modelo más rápido y económico de la familia GPT-4
        messages=messages,          # Historial de conversación
        temperature=0.7,            # Creatividad media en las respuestas
        max_tokens=150              # Límite de longitud de respuesta
    )
    return response.choices[0].message.content.strip()  # Devuelve solo el texto de la respuesta
