# recordatorio.py
# Módulo encargado de gestionar los recordatorios y alertas personalizadas del usuario.
# Permite a los usuarios establecer recordatorios de eventos o actividades importantes y recibir notificaciones sobre ellos.
# Utiliza la función `Streamlit` para gestionar la interfaz y el estado de sesión para almacenar los recordatorios del usuario.
# Este módulo también permite eliminar recordatorios según las necesidades del usuario.

import streamlit as st
import datetime
import calendar

# Función para mostrar recordatorios
def mostrar_recordatorios(seleccion):
    if seleccion == "Recordatorios":
        st.markdown("#### 📅 Recordatorios")

        # Inicializar lista en sesión
        if "recordatorios" not in st.session_state:
            st.session_state.recordatorios = []

        # Estado para mostrar u ocultar el formulario de carga
        if "mostrar_formulario" not in st.session_state:
            st.session_state.mostrar_formulario = False

        # Mostrar lista de recordatorios
        if st.session_state.recordatorios:
            st.markdown("### 📖 Tus recordatorios:")
            for i, r in enumerate(st.session_state.recordatorios):
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.markdown(f"**{i + 1}.** {r['fecha']} a las {r['hora']} - {r['descripcion']}")
                with col2:
                    if st.button("❌", key=f"del_{i}"):
                        st.session_state.recordatorios.pop(i)
                        st.rerun()
        else:
            st.info("Aún no cargaste ningún recordatorio.")

        # Botón para mostrar formulario
        if not st.session_state.mostrar_formulario:
            if st.button("➕ Añadir recordatorio"):
                st.session_state.mostrar_formulario = True

        # Formulario para nuevo recordatorio
        if st.session_state.mostrar_formulario:
            st.markdown("---")
            st.markdown("### ➕ Nuevo Recordatorio")

            descripcion = st.text_input("📝 Escribí el recordatorio:")

            # Calendario en español y dinámico
            meses_es = {
                "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
                "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
                "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
            }
            anio_actual = datetime.datetime.now().year
            anios = list(range(anio_actual, anio_actual + 3))

            col1, col2, col3 = st.columns(3)
            with col2:
                mes_nombre = st.selectbox("📅 Mes", list(meses_es.keys()))
            with col3:
                anio = st.selectbox("📅 Año", anios)
            with col1:
                mes_num = meses_es[mes_nombre]
                dias_mes = calendar.monthrange(anio, mes_num)[1]
                dias = list(range(1, dias_mes + 1))
                dia = st.selectbox("📅 Día", dias)

            fecha = datetime.date(anio, mes_num, dia)
            hora = st.time_input("⏰ Seleccioná la hora:")

            col4, col5 = st.columns(2)
            with col4:
                if st.button("💾 Guardar"):
                    if descripcion:
                        nuevo = {
                            "descripcion": descripcion,
                            "fecha": fecha.strftime("%d/%m/%Y"),
                            "hora": hora.strftime("%H:%M")
                        }
                        st.session_state.recordatorios.append(nuevo)
                        st.success("✅ Recordatorio guardado.")
                        st.session_state.mostrar_formulario = False
                        st.rerun()
                    else:
                        st.warning("Por favor, escribí una descripción.")
            with col5:
                if st.button("❌ Cancelar"):
                    st.session_state.mostrar_formulario = False
                    st.rerun()