# recordatorio.py
# Módulo encargado de gestionar la funcionalidad de recordatorios en la aplicación.
# Permite visualizar, agregar y eliminar recordatorios personalizados por el usuario.

import streamlit as st
import datetime

# Muestra la sección interactiva de recordatorios en la interfaz
def mostrar_recordatorios(seleccion):
    if seleccion == "Recordatorios":
        st.markdown("#### 📅 Recordatorios")

        # Inicializa la lista de recordatorios si no existe
        if "recordatorios" not in st.session_state:
            st.session_state.recordatorios = []

        # Inicializa el estado del formulario si no existe
        if "mostrar_formulario" not in st.session_state:
            st.session_state.mostrar_formulario = False

        # Muestra los recordatorios existentes con opción a eliminar
        if st.session_state.recordatorios:
            st.markdown("### 📖 Tus recordatorios:")
            for i, r in enumerate(st.session_state.recordatorios):
                with st.expander(f"{r['fecha']} a las {r['hora']} - {r['descripcion']}"):
                    if st.button("Eliminar recordatorio", key=f"del_{i}"):
                        st.session_state.recordatorios.pop(i)
                        st.success("Recordatorio eliminado.")
                        st.rerun()
        else:
            st.info("Aún no cargaste ningún recordatorio.")

        # Botón para habilitar el formulario de nuevo recordatorio
        if not st.session_state.mostrar_formulario:
            if st.button("➕ Añadir recordatorio"):
                st.session_state.mostrar_formulario = True

        # Formulario para cargar un nuevo recordatorio
        if st.session_state.mostrar_formulario:
            st.markdown("---")
            st.markdown("### ➕ Nuevo Recordatorio")

            descripcion = st.text_input("📝 Escribí el recordatorio:")
            fecha = st.date_input("📅 Seleccioná la fecha:", min_value=datetime.date.today())

            # Selección personalizada de hora y minuto
            horas = [f"{h:02d}" for h in range(24)]
            minutos = ["00", "15", "30", "45"]

            col1, col2 = st.columns(2)
            with col1:
                hora_sel = st.selectbox("Hora", horas)
            with col2:
                minuto_sel = st.selectbox("Minuto", minutos)

            hora_formateada = f"{hora_sel}:{minuto_sel}"

            # Botones de acción: guardar o cancelar
            col3, col4 = st.columns(2)
            with col3:
                if st.button("💾 Guardar"):
                    if descripcion:
                        nuevo = {
                            "descripcion": descripcion,
                            "fecha": fecha.strftime("%d/%m/%Y"),
                            "hora": hora_formateada
                        }
                        st.session_state.recordatorios.append(nuevo)
                        st.success("✅ Recordatorio guardado.")
                        st.session_state.mostrar_formulario = False
                        st.rerun()
                    else:
                        st.warning("Por favor, escribí una descripción.")
            with col4:
                if st.button("❌ Cancelar"):
                    st.session_state.mostrar_formulario = False
                    st.rerun()

# Devuelve un resumen textual de los recordatorios para ser usado en el asistente virtual
def obtener_texto_recordatorios(recordatorios):
    if recordatorios and len(recordatorios) > 0:
        if len(recordatorios) == 1:
            r = recordatorios[0]
            return f"📅 Tenés un recordatorio para el día {r['fecha']} a las {r['hora']}, para {r['descripcion'].lower()}."
        else:
            lineas = ["📅 Tenés varios recordatorios programados:"]
            for r in recordatorios:
                lineas.append(f"- El {r['fecha']} a las {r['hora']}, para {r['descripcion'].lower()}.")
            return "\n".join(lineas)
    else:
        return "No tienes recordatorios pendientes por ahora. ¡Aprovechá para organizar tu día! 😊"
