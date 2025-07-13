# tts.py
# Módulo encargado de convertir texto en audio usando la API de Google Text-to-Speech
# y reproducir la voz del asistente en la aplicación.

import streamlit as st
from google.cloud import texttospeech
from google.oauth2 import service_account
import re

# Elimina emojis y caracteres no verbales del texto antes de pasarlo a TTS
def limpiar_texto_para_tts(texto):
    return re.sub(r'[^\w\s.,!?¿¡:;áéíóúÁÉÍÓÚñÑ]', '', texto)


credentials = service_account.Credentials.from_service_account_info(
    dict(st.secrets["gcp_tts"])
)

# Crea un cliente autenticado para utilizar Google Text-to-Speech
def crear_cliente_tts():
    return texttospeech.TextToSpeechClient(credentials=credentials)

# Convierte un texto en audio (formato MP3) utilizando la voz masculina en español de Argentina
def sintetizar_texto(texto, cliente):
    input_text = texttospeech.SynthesisInput(text=texto)
    voz = texttospeech.VoiceSelectionParams(
        language_code="es-AR",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    respuesta = cliente.synthesize_speech(
        input=input_text, voice=voz, audio_config=audio_config
    )
    return respuesta.audio_content

# Obtiene el último mensaje del asistente, lo sintetiza y lo guarda en session_state
def reproducir_audio_y_guardar():
    if "messages" not in st.session_state or not st.session_state["messages"]:
        st.warning("No hay mensajes para reproducir.")
        return

    # Buscar el último mensaje generado por el asistente
    ultimo_mensaje = next(
        (msg["content"] for msg in reversed(st.session_state["messages"]) if msg["role"] == "assistant"),
        None
    )

    if not ultimo_mensaje:
        st.warning("No hay mensajes de la IA para reproducir.")
        return

    try:
        cliente = crear_cliente_tts()
        texto_limpio = limpiar_texto_para_tts(ultimo_mensaje)
        audio_bytes = sintetizar_texto(texto_limpio, cliente)
        st.session_state["audio_abu"] = audio_bytes
        print("✅ Audio generado y guardado en session_state.")
    except Exception as e:
        st.error(f"Error al generar el audio: {e}")
        print("❌ Error en TTS:", e)


# Muestra un botón para generar el audio del último mensaje del asistente
def boton_reproducir():
    if "tts_reproduciendo" not in st.session_state:
        st.session_state.tts_reproduciendo = False

    def on_click():
        st.session_state.tts_reproduciendo = True
        reproducir_audio_y_guardar()
        st.session_state.tts_reproduciendo = False

    # Botón de reproducción
    if st.button("🔊", on_click=on_click, key="boton_reproducir_abu"):
        pass

    if st.session_state.tts_reproduciendo:
        st.markdown("<span style='color:green'>Reproduciendo...</span>", unsafe_allow_html=True)
