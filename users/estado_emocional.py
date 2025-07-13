# estado_emocional.py
# Módulo encargado de permitir al usuario seleccionar su estado emocional actual.
# Guarda esta información en session_state para personalizar la conversación.

import streamlit as st


# --- Función principal para mostrar el selector emocional ---
def seleccionar_estado_emocional():
    # Inicializar el estado emocional si no está presente
    if "estado_emocional" not in st.session_state:
        st.session_state.estado_emocional = None

    # Diccionario de emociones disponibles con su emoji asociado
    emociones = {
        "Neutral": "😐",
        "Pensando": "🤔",
        "Feliz": "😄",
        "Sin ánimo": "😒",
        "Triste": "😔"
    }

    # Si el estado emocional no fue seleccionado aún, mostrar opciones
    if st.session_state.estado_emocional is None:
        st.markdown("### 💬 ¿Cómo te sentís hoy?")

        # Crear columnas para los botones de emociones
        cols = st.columns(len(emociones))

        # Mostrar un botón por cada emoción (emoji + texto)
        for idx, (emocion, emoji) in enumerate(emociones.items()):
            if cols[idx].button(f"{emoji}\n{emocion}", key=f"emocion_{emocion}"):
                # Guardar emoción seleccionada en minúsculas
                st.session_state.estado_emocional = emocion.lower()
                st.success(f"Gracias por compartir cómo te sentís 😊")
                st.rerun()  # Reinicia la app para aplicar cambios

    else:
        # Si ya se seleccionó, mostrar el estado actual
        emocion = st.session_state.estado_emocional.capitalize()
        emoji = emociones.get(emocion, "")
        st.markdown(f"### Tu estado de ánimo hoy es: **{emocion} {emoji}**")


# --- Permite ejecutar el módulo de forma independiente para pruebas ---
if __name__ == "__main__":
    seleccionar_estado_emocional()
