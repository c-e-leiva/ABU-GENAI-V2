# emergencia.py
# Módulo encargado de manejar la sección de emergencia en la aplicación.
# Permite al usuario visualizar sus datos de contacto de emergencia y obra social,
# y enviar una alerta en caso de necesitar ayuda urgente.

import streamlit as st

# Muestra la interfaz de emergencia cuando el usuario selecciona esa opción
def mostrar_emergencia(seleccion, nombre):
    if seleccion == "Emergencia":
        st.subheader("🚨 Emergencia")
        st.write("Presioná el botón de emergencia para contactar a tu persona de confianza.")

        # Mostrar información del contacto de emergencia si está disponible
        st.markdown("### 👤 Contacto de emergencia")
        contacto = st.session_state.get("contacto_emergencia")
        if contacto:
            st.info(
                f"**Nombre:** {contacto['nombre']}\n\n"
                f"**Teléfono:** {contacto['numero']}\n\n"
                f"**Relación:** {contacto['relacion']}"
            )
        else:
            st.warning("⚠️ No se ha registrado un contacto de emergencia.")

        # Mostrar información de la obra social o prepaga
        st.markdown("### 🏥 Obra social / Prepaga")
        obra = st.session_state.get("obra_social")
        if obra:
            st.info(
                f"**Obra social:** {obra['nombre']}\n\n"
                f"**Teléfono:** {obra['telefono']}"
            )
        else:
            st.warning("⚠️ No se ha registrado una obra social o prepaga.")

        # Inicializar la bandera para mostrar la confirmación de alerta
        if "mostrar_confirmacion" not in st.session_state:
            st.session_state.mostrar_confirmacion = False

        # Botón para iniciar solicitud de ayuda
        if st.button("📞 Solicitar ayuda"):
            st.session_state.mostrar_confirmacion = True

        # Confirmación antes de enviar la alerta
        if st.session_state.mostrar_confirmacion:
            with st.container():
                provincia = st.session_state.get("provincia", "ubicación no disponible")
                mensaje = (
                    f"🚨 Hola, soy ABU, el asistente virtual de **{nombre}**.\n\n"
                    f"Está necesitando ayuda urgente y te tiene como contacto de emergencia.\n"
                    f"📍 *Ubicación estimada: {provincia}, Argentina*"
                )
                st.warning(mensaje)

                # Simulación del envío de alerta
                if st.button("✅ Enviar alerta"):
                    st.success("✅ ¡Alerta enviada con éxito! Mantené la calma, tu contacto de emergencia ya fue notificado y te ayudará lo antes posible.")
                    st.session_state.mostrar_confirmacion = False
