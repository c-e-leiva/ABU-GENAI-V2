# core/detectar_emergencia.py
# Módulo encargado de detectar situaciones de emergencia en los mensajes escritos por el usuario,
# utilizando un modelo de lenguaje (LLM) a través de LangChain.
# Emplea un LLMChain (LangChain) que envía un prompt estructurado al modelo GPT
# y espera una respuesta cerrada ("Sí" o "No") indicando si se trata de una situación urgente.

from langchain.output_parsers import RegexParser
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from openai import OpenAI
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI


# Inicializa el modelo GPT-3.5-turbo con temperatura baja para respuestas más coherentes y deterministas
llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")

# Detecta si el texto del usuario indica una emergencia
def detectar_emergencia(texto_usuario: str) -> bool:
    """
    Usa un chain simple para detectar si hay una situación de emergencia en el mensaje del usuario.
    """
    # Plantilla de prompt que pide una respuesta 'Sí' o 'No' basada en el mensaje
    template = """
    Analizá el siguiente mensaje de una persona mayor y respondé solo con 'Sí' o 'No'.

    ¿Está pidiendo ayuda urgente o hay alguna situación que pueda considerarse una emergencia?

    Mensaje:
    {mensaje}

    Respuesta:
    """
    # Construye el prompt con el template
    prompt = PromptTemplate.from_template(template)

    # Define el chain que ejecuta el LLM con el prompt
    chain = LLMChain(llm=llm, prompt=prompt)

    # Ejecuta el chain con el texto del usuario y procesa la respuesta
    respuesta = chain.run(mensaje=texto_usuario).strip().lower()

    # Devuelve True si la respuesta contiene 'sí' indicando emergencia
    return "sí" in respuesta
