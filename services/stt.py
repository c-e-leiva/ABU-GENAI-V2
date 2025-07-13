# stt.py
# Módulo encargado de capturar entrada de voz del usuario mediante micrófono
# y convertirla en texto utilizando el componente de Streamlit.

from streamlit_mic_recorder import speech_to_text

# Transcribe la voz capturada desde el micrófono y la convierte en texto
def transcribir_con_microfono():
    texto = speech_to_text(
        language='es',                  # Idioma en español
        start_prompt="🎤",              # Texto del botón para iniciar
        stop_prompt="🛑 Detener",       # Texto del botón para detener
        just_once=True,                 # Graba una vez, no en bucle
        use_container_width=True,       # Usa el ancho completo del contenedor
        key="abu_stt"                   # Clave para mantener el estado
    )
    return texto
