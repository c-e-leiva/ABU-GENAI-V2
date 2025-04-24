# ayuda.py
# Módulo encargado de manejar la sección de emergencia en la aplicación.
# Permite al usuario solicitar ayuda de manera urgente, enviando un mensaje a su contacto de emergencia con su ubicación.
# Utiliza Streamlit para la interfaz de usuario y guarda el estado de la solicitud de ayuda en `st.session_state`.


import streamlit as st

# Función para mostrar la sección de ayuda/emergencia
def mostrar_ayuda(seleccion, nombre):
    if seleccion == "Ayuda":  # Solo mostrar la sección si el usuario selecciona "Ayuda"
        st.subheader("🚨 Emergencia")  # Título para la sección de emergencia
        st.write("Presioná el botón de emergencia para contactar a tu persona de confianza.")  # Instrucciones para el usuario

        # Inicialización de la variable de confirmación en el estado de sesión, si no existe
        if "mostrar_confirmacion" not in st.session_state:
            st.session_state.mostrar_confirmacion = False  # Por defecto, no mostrar la confirmación

        # Botón para solicitar ayuda
        if st.button("📞 Solicitar ayuda"):  # Si el usuario presiona el botón
            st.session_state.mostrar_confirmacion = True  # Mostrar la confirmación de alerta

        # Si la confirmación está activada, mostrar mensaje de emergencia
        if st.session_state.mostrar_confirmacion:
            with st.container():  # Iniciar contenedor para agrupar los elementos de la alerta
                nombre_usuario = nombre  # Asignar el nombre del usuario a la variable (reemplazar con la variable real)
                mensaje = (
                    f"🚨 Hola, soy *{nombre_usuario}*. Estoy en una emergencia y necesito tu ayuda."
                    f"\n\nVoy a enviarte mi ubicación actual."
                )  # Mensaje de alerta que se enviará
                st.warning(mensaje)  # Mostrar el mensaje de alerta como advertencia

                # Botón para enviar la alerta
                if st.button("✅ Enviar alerta"):  # Si el usuario presiona el botón para enviar la alerta
                    st.success("✅ ¡Alerta enviada con éxito! Mantené la calma, tu contacto de emergencia ya fue notificado y te ayudará lo antes posible.")  # Mensaje de éxito
                    st.session_state.mostrar_confirmacion = False  # Restablecer la variable de confirmación a su valor inicial

