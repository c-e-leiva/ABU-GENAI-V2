# perfil_usuario.py
# Módulo para gestionar el perfil del usuario, datos de emergencia y preferencias.

# Construye y retorna un diccionario consolidado con los datos del perfil del usuario,
# incluyendo información personal, estado emocional y preferencias configuradas.
def construir_perfil_usuario(session_state):
    dificultades_dict = session_state.get("dificultades", {})
    dificultades_list = [k for k, v in dificultades_dict.items() if v]

    perfil = {
        "nombre": session_state.get("nombre", ""),
        "edad": session_state.get("edad", 0),
        "provincia": session_state.get("provincia", ""),
        "descripcion": session_state.get("descripcion", ""),
        "vive_solo": session_state.get("vive_solo", ""),
        "dificultades": dificultades_list,
        "estado_emocional": session_state.get("estado_emocional", "Neutral"),
        "preferencias": session_state.get("preferencias", {})
    }
    return perfil

# Construye un diccionario con la información de contacto de emergencia
# y datos de obra social, obtenidos del estado de la sesión.
def construir_datos_emergencia(session_state):
    contacto_emergencia = session_state.get("contacto_emergencia", {})
    obra_social = session_state.get("obra_social", {})

    datos_emergencia = {
        "contacto_emergencia": {
            "nombre": contacto_emergencia.get("nombre", ""),
            "numero": contacto_emergencia.get("numero", ""),
            "relacion": contacto_emergencia.get("relacion", "")
        },
        "obra_social": {
            "nombre": obra_social.get("nombre", ""),
            "telefono": obra_social.get("telefono", "")
        }
    }
    return datos_emergencia

# Retorna el historial completo de mensajes de la conversación almacenados en la sesión.
def construir_historial_conversacion(session_state):
    return session_state.get("messages", [])

# Retorna la lista actual de recordatorios almacenados en el estado de sesión.
def construir_recordatorios(session_state):
    return session_state.get("recordatorios", [])

# Exporta un diccionario unificado que contiene toda la información relevante del usuario:
# perfil, datos de emergencia, historial de conversación y recordatorios.
def exportar_perfil_completo(session_state):
    return {
        "perfil": construir_perfil_usuario(session_state),
        "preferencias": session_state.get("preferencias", {}),
        "emergencia": construir_datos_emergencia(session_state),
        "historial": construir_historial_conversacion(session_state),
        "recordatorios": construir_recordatorios(session_state)
    }
