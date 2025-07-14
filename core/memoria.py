# memoria.py

# Importa la memoria conversacional de LangChain y herramientas de Streamlit
from langchain.memory import ConversationBufferMemory
import streamlit as st

# Diccionario que guarda una instancia de memoria conversacional por usuario
_memorias_por_usuario = {}

# Obtiene el nombre del usuario activo desde el estado de sesión
def obtener_usuario_activo():
    return st.session_state.get("nombre", "desconocido")

# Devuelve la memoria conversacional del usuario actual; si no existe, la crea
def obtener_memoria_conversacional():
    usuario = obtener_usuario_activo()
    if usuario not in _memorias_por_usuario:
        _memorias_por_usuario[usuario] = ConversationBufferMemory(
            return_messages=False,
            memory_key="history"
        )
    return _memorias_por_usuario[usuario]

# Agrega un mensaje (de usuario o de ABU) a la memoria conversacional
def agregar_mensaje_a_memoria(role: str, content: str):
    memoria = obtener_memoria_conversacional()
    if role == "user":
        memoria.chat_memory.add_user_message(content)
    elif role == "assistant":
        memoria.chat_memory.add_ai_message(content)

# Guarda también el mensaje en un historial simplificado (resumen), por usuario
def agregar_mensaje_resumen(role, content):
    agregar_mensaje_a_memoria(role, content)
    usuario = obtener_usuario_activo()
    key = f"historial_resumen_{usuario}"
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].append({"role": role, "content": content})

# Devuelve el historial resumen del usuario actual, o el historial conversacional completo si no hay resumen
def obtener_historial_resumen():
    usuario = obtener_usuario_activo()
    key = f"historial_resumen_{usuario}"
    if key in st.session_state and st.session_state[key]:
        lines = []
        for msg in st.session_state[key]:
            prefix = "Usuario" if msg["role"] == "user" else "ABU"
            lines.append(f"{prefix}: {msg['content']}")
        return "\n".join(lines)

    # Si no hay resumen, devuelve el historial completo desde LangChain
    memoria = obtener_memoria_conversacional()
    return memoria.load_memory_variables({}).get("history", "")

# Elimina la memoria conversacional guardada para un usuario específico
def limpiar_memoria_usuario(usuario: str):
    """Elimina la memoria conversacional del usuario especificado."""
    _memorias_por_usuario.pop(usuario, None)
