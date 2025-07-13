# conversacion.py
# Módulo encargado de gestionar el modo de conversación con ABU, integrando entrada/salida por texto y voz, 
# análisis de emociones, detección de intenciones y respuestas generadas por OpenAI.

import streamlit as st  # Interfaz de usuario con Streamlit

# Módulos centrales del asistente (gestión de prompts y comunicación con OpenAI)
from core.prompt_manager import generar_mensajes, detectar_afecto_o_emocion, detectar_intencion_extra
from core.openai_service import obtener_respuesta

# Servicios externos para entrada y salida de voz
from services.stt import transcribir_con_microfono
from services.tts import boton_reproducir, reproducir_audio_y_guardar

# Funciones auxiliares para manejar recordatorios y noticias
from features.recordatorio import obtener_texto_recordatorios
from features.noticias import obtener_texto_clima, obtener_texto_noticias

# Detección de emergencia (LangChain u otra lógica)
from core.detectar_emergencia import detectar_emergencia

# Manejo de memoria conversacional
from core.memoria import agregar_mensaje_a_memoria


# Función auxiliar para enviar dos mensajes automáticos en caso de emergencia:
# uno simula notificar al contacto de emergencia y otro tranquiliza al usuario.
def enviar_mensajes_emergencia(perfil_usuario):
    contacto = st.session_state.get("contacto_emergencia", {})
    nombre_contacto = contacto.get("nombre", "tu contacto")
    ubicacion = perfil_usuario.get("provincia", "su ubicación")
    nombre_usuario = perfil_usuario.get("nombre", "el usuario")

    # Mensaje que ABU envia al contacto de emergencia
    mensaje_cartel = (
        f"🚨 Hola, soy ABU, el asistente virtual de {nombre_usuario}.\n\n"
        f"Está necesitando tu ayuda urgente y te tiene como contacto de emergencia. "
        f"📍 Su Ubicación estimada es: {ubicacion}"
    )

    # Mensaje que ABU le dice al usuario
    mensaje_para_usuario = (
        f"Ya envié un aviso a {nombre_contacto}, tu contacto de emergencia. "
        "Mantené la calma, tu contacto de emergencia ya fue notificado y te ayudará lo antes posible.\n"
        "¿Querés reenviar la alerta? ¿sí - no?"
    )

    st.session_state["messages"].append({"role": "assistant", "content": mensaje_cartel})
    st.session_state["messages"].append({"role": "assistant", "content": mensaje_para_usuario})
    st.rerun()


# Función principal que gestiona el flujo completo de la conversación:
# muestra historial, recibe entrada por texto o voz, detecta emociones e intenciones,
# y genera respuestas usando el modelo de lenguaje.

def iniciar_conversacion(seleccion, perfil_usuario, client, openweather_api_key=None):
    if seleccion != "Conversar":
        return

    st.markdown("#### 🔡️ **Modo Conversación**")

    # Inicializa el historial si es la primera vez
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["conversacion_iniciada"] = False


    # Muestra cada mensaje anterior (incluyendo opción de reproducir audio si existe)
    for i, msg in enumerate(st.session_state["messages"]):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            if (
                msg["role"] == "assistant"
                and i == len(st.session_state["messages"]) - 1
                and "audio_abu" in st.session_state
            ):
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.audio(st.session_state["audio_abu"], format="audio/mp3")
                with col2:
                    if st.button("❌", key=f"eliminar_audio_{i}"):
                        del st.session_state["audio_abu"]
                        st.rerun()

    # Captura entrada del usuario: texto, micrófono o botón de voz
    col1, col2, col3 = st.columns([7, 1, 1])
    with col1:
        nuevo_mensaje = st.chat_input("Escribime tu mensaje…")
    with col2:
        texto_voz = transcribir_con_microfono() or ""
        if texto_voz:
            nuevo_mensaje = texto_voz
    with col3:
        boton_reproducir()

    # Procesamiento del nuevo mensaje ingresado
    if nuevo_mensaje:
        es_inicial = not st.session_state["conversacion_iniciada"]
        st.session_state["conversacion_iniciada"] = True

        # Guarda el mensaje del usuario
        st.session_state["messages"].append({"role": "user", "content": nuevo_mensaje})

        agregar_mensaje_a_memoria("user", nuevo_mensaje)


        # Detecta emoción en el mensaje (usado para adaptar la respuesta)
        tipo_emocion = detectar_afecto_o_emocion(nuevo_mensaje) or "neutral"

        # Detecta si el usuario pide funciones como noticias, clima o recordatorios
        intencion_extra = detectar_intencion_extra(nuevo_mensaje)

        # Muestra noticias si se detectó la intención
        if intencion_extra == "noticias":
            texto_noticias = obtener_texto_noticias()
            st.session_state["messages"].append({"role": "assistant", "content": texto_noticias})
            st.rerun()
            return

        # Muestra clima según provincia si se detectó la intención
        if intencion_extra == "clima":
            provincia = perfil_usuario.get("provincia", "")
            texto_clima = obtener_texto_clima(provincia, openweather_api_key)
            st.session_state["messages"].append({"role": "assistant", "content": texto_clima})
            st.rerun()
            return

        # Muestra recordatorios si se detectó la intención
        if intencion_extra == "recordatorios":
            recordatorios = st.session_state.get("recordatorios", [])
            texto_recordatorios = obtener_texto_recordatorios(recordatorios)
            st.session_state["messages"].append({"role": "assistant", "content": texto_recordatorios})
            st.rerun()
            return

        # 🚨 Lógica para emergencia (puede detectar o confirmar reenvío)
        if st.session_state.get("modo_emergencia", False):
            if nuevo_mensaje.strip().lower() in ["sí", "si","SI", "reenviar", "s", "enviar de nuevo","ENVIAR","enviar"]:
                enviar_mensajes_emergencia(perfil_usuario)
                return
            elif nuevo_mensaje.strip().lower() in ["no", "salir", "cancelar", "ya está","n"]:
                st.session_state["modo_emergencia"] = False
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": "Perfecto, salimos del modo de emergencia. Estoy acá si necesitás otra cosa. 💙"
                })
                st.rerun()
                return

        # Si detecta una emergencia nueva
        elif detectar_emergencia(nuevo_mensaje):
            st.session_state["modo_emergencia"] = True
            enviar_mensajes_emergencia(perfil_usuario)
            return

        # 🧠 Arma el contexto para que el modelo responda considerando el perfil y la emoción
        mensajes = generar_mensajes(
            perfil=perfil_usuario,
            mensaje_usuario=nuevo_mensaje,
            es_inicial=es_inicial,
            tipo_emocion=tipo_emocion,
            historial=st.session_state["messages"][:-1],
        )

        # Obtiene la respuesta del modelo (usando OpenAI)
        respuesta = obtener_respuesta(client, mensajes)

         # Guarda y muestra la respuesta + agregar a memoria
        st.session_state["messages"].append({"role": "assistant", "content": respuesta})

        agregar_mensaje_a_memoria("assistant", respuesta)

        # Vuelve a mostrar la conversación con el nuevo mensaje
        st.rerun()
