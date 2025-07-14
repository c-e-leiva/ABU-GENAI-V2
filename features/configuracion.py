# configuracion.py
# Módulo encargado de mostrar y gestionar la configuración del usuario,
# incluyendo perfil, preferencias, historial, datos de emergencia y opciones para guardar o cerrar sesión.

from storage import exportar_sheets
from storage.resumen_historial import generar_resumen
from openai import OpenAI
import streamlit as st
from core.memoria import limpiar_memoria_usuario



# Inicializa cliente OpenAI con la clave API segura desde secrets
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Función principal que controla la interfaz de configuración del usuario
def mostrar_configuracion(datos):
    import streamlit as st
    from storage import exportar_sheets

    # Lee la clave secreta para controlar acceso a la configuración
    CLAVE_SECRETA = st.secrets["CLAVE_SECRETA"]

    # Estado para controlar si el usuario tiene acceso a configuración
    if "acceso_config" not in st.session_state:
        st.session_state.acceso_config = False

    # Solicita clave de acceso si no está autenticado
    if not st.session_state.acceso_config:
        clave = st.text_input("🔐 Ingresá la clave para acceder a configuración", type="password")
        if st.button("Entrar"):
            if clave == CLAVE_SECRETA:
                st.session_state.acceso_config = True
                st.rerun()  # Recarga la app tras autenticación exitosa
            else:
                st.error("Clave incorrecta, intentá de nuevo.")
        return  # No continúa sin autenticación

    # Extrae datos del perfil, emergencia, preferencias, historial y recordatorios
    perfil = datos.get("perfil", {})
    emergencia = datos.get("emergencia", {})
    preferencias = datos.get("preferencias", {})
    historial = datos.get("historial", [])
    recordatorios = datos.get("recordatorios", [])

    contacto = emergencia.get("contacto_emergencia", {})
    obra_social = emergencia.get("obra_social", {})

    # Título sección configuración
    st.markdown("## ⚙️ Configuración del usuario")

    # Muestra datos básicos del perfil con valores por defecto si no están definidos
    st.markdown(f"**👤 Nombre:** {perfil.get('nombre', 'No definido')}")
    st.markdown(f"**🎂 Edad:** {perfil.get('edad', 'No definida')}")
    st.markdown(f"**📍 Provincia:** {perfil.get('provincia', 'No definida')}")
    st.markdown(f"**📝 Descripción:** {perfil.get('descripcion', 'No definida')}")
    st.markdown(f"**🏠 Vive solo:** {perfil.get('vive_solo', 'No definido')}")
    st.markdown(f"**😊 Estado emocional:** {perfil.get('estado_emocional', 'Neutral')}")

    # Muestra preferencias activas en forma legible
    prefs_activas = [k.capitalize() for k, v in preferencias.items() if v]
    st.markdown("**✅ Preferencias activas:** " + (", ".join(prefs_activas) if prefs_activas else "Ninguna"))

    # Muestra dificultades reportadas o mensaje si no hay
    dificultades = perfil.get("dificultades", [])
    st.markdown("**⚠️ Dificultades:** " + (", ".join(dificultades) if dificultades else "Ninguna"))

    st.markdown("---")

    # Lista los recordatorios si existen
    st.markdown("### ⏰ Recordatorios:")
    if recordatorios:
        for r in recordatorios:
            st.markdown(f"- {r['fecha']} a las {r['hora']}: {r['descripcion']}")
    else:
        st.info("No hay recordatorios cargados.")

    st.markdown("---")

    # Muestra primeros 5 mensajes del historial de conversación
    st.markdown("### 💬 Historial de conversación:")
    if historial:
        primeros_mensajes = historial[:5]
        for m in primeros_mensajes:
            st.markdown(f"**{m['role'].capitalize()}**: {m['content']}")
        if len(historial) > 5:
            st.info(f"Y {len(historial) - 5} mensajes más...")
    else:
        st.info("Todavía no hay mensajes registrados.")

    st.markdown("---")

    # Sección para generar y mostrar resumen del historial
    
    # Sección para generar y mostrar resumen del historial
    st.markdown("### 📝 Generar resumen del historial")

    # 🧠 Clave única por usuario para el resumen
    usuario = st.session_state.get("nombre", "").strip().lower()
    key_resumen = f"resumen_chat_{usuario}"

    # Botón para generar resumen usando OpenAI
    if st.button("🧠 Generar resumen de la conversación"):
        resumen = generar_resumen(client)
        st.session_state[key_resumen] = resumen

    # Mostrar el resumen si ya fue generado
    if key_resumen in st.session_state:
        st.markdown("### 🧠 Resumen generado:")
        st.success(st.session_state[key_resumen])


    st.markdown("---")


    # Muestra contacto de emergencia o aviso si no está definido
    st.markdown("### 🚨 Contacto de emergencia:")
    if contacto.get("nombre"):
        st.markdown(f"- {contacto['nombre']} ({contacto['relacion']}): {contacto['numero']}")
    else:
        st.info("No se registró un contacto de emergencia.")
    
    st.markdown("---")

    # Muestra datos de obra social o prepaga o mensaje si no existe
    st.markdown("### 🏥 Obra social / Prepaga:")
    if obra_social.get("nombre") or obra_social.get("telefono"):
        st.markdown(f"- **Nombre:** {obra_social.get('nombre', 'No registrado')}")
        st.markdown(f"- **Teléfono:** {obra_social.get('telefono', 'No registrado')}")
    else:
        st.info("No se registró ninguna obra social o prepaga.")

    st.markdown("---")

    # Botones para cerrar sesión o guardar datos en Google Sheets
    col1, col2 = st.columns(2)
    with col1:
        # Botón para cerrar sesión: limpia variables de sesión y recarga la app
        if st.button("Cerrar sesión"):
            usuario = st.session_state.get("nombre", "").strip().lower()

            limpiar_memoria_usuario(usuario)
            st.session_state.pop(f"historial_resumen_{usuario}", None)

            claves_a_borrar = [
                "nombre", "edad", "provincia", "descripcion", "vive_solo", "dificultades",
                "estado_emocional", "preferencias", "contacto_emergencia", "obra_social",
                "opcion", "config_extra_completada", "modo_nuevo_usuario", "acceso_config", "recordatorios"
            ]
            for key in claves_a_borrar:
                st.session_state.pop(key, None)

            st.session_state.pop("messages", None)  # 💥 historial de conversación
            st.session_state.pop("conversacion_iniciada", None)

            st.rerun()


    with col2:
        # Botón para guardar datos en Google Sheets usando la función exportar_todo
        if st.button("Guardar"):
            spreadsheet_id = st.secrets["SPREADSHEET_ID"]
            # Esta línea asigna el resumen generado para ser guardado junto a los datos
            datos["resumen"] = st.session_state.get(f"resumen_chat_{usuario}", "")
            id_usr = exportar_sheets.exportar_todo(spreadsheet_id=spreadsheet_id, datos=datos)
            st.success(f"✅ Datos guardados correctamente. ID usuario: `{id_usr}`")
            st.markdown(f"[📄 Ver hoja en Google Sheets](https://docs.google.com/spreadsheets/d/{spreadsheet_id})")
