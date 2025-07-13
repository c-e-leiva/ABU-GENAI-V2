# memoria.py
# Módulo para gestionar la memoria conversacional del asistente usando LangChain y Streamlit

from langchain.memory import ConversationBufferMemory
import streamlit as st

# Memoria conversacional de LangChain
# Memoria global de la conversación que almacena los mensajes intercambiados

memoria_global = ConversationBufferMemory(return_messages=False, memory_key="history")

# Devuelve la memoria conversacional global
def obtener_memoria_conversacional():
    return memoria_global

# Agrega un mensaje a la memoria (rol: user o assistant)
def agregar_mensaje_a_memoria(role: str, content: str):
    if role == "user":
        memoria_global.chat_memory.add_user_message(content)
    elif role == "assistant":
        memoria_global.chat_memory.add_ai_message(content)

# Agrega un mensaje a la memoria y al historial resumen en session_state
def agregar_mensaje_resumen(role, content):
    agregar_mensaje_a_memoria(role, content)
    if "historial_resumen" not in st.session_state:
        st.session_state["historial_resumen"] = []
    st.session_state["historial_resumen"].append({"role": role, "content": content})

# Obtiene el historial resumen como string con prefijos Usuario o ABU
def obtener_historial_resumen():
    if "historial_resumen" in st.session_state and st.session_state["historial_resumen"]:
        lines = []
        for msg in st.session_state["historial_resumen"]:
            prefix = "Usuario" if msg["role"] == "user" else "ABU"
            lines.append(f"{prefix}: {msg['content']}")
        return "\n".join(lines)
    return memoria_global.load_memory_variables({}).get("history", "")
