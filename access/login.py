# login.py

# --- Librerías necesarias ---
import streamlit as st               # Para construir la interfaz web
from PIL import Image               # Para abrir imágenes locales (logo)
import base64                       # Para convertir imagen en base64 (usada en HTML)

# --- Funciones del sistema ---
from storage.perfil_usuario import exportar_perfil_completo   # Exportar perfil completo 
from users.perfiles_precargados import obtener_perfil      # Función para obtener perfiles existentes

# --- Clave secreta definida en .streamlit/secrets.toml  ---
CLAVE_SECRETA = st.secrets["CLAVE_SECRETA"]


# --- Función auxiliar para convertir imagen local a base64 (necesario para mostrarla centrada en HTML) ---
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# --- Función principal que muestra la interfaz de login ---
def mostrar_login():
    # Configura el título de la pestaña del navegador y centra la app
    st.set_page_config(page_title="ABU - Iniciar sesión", layout="centered")

    # Carga el logo y lo convierte a base64 para insertarlo en HTML
    logo_base64 = get_image_base64("assets/img/logo.png")

    # --- Encabezado visual centrado con logo y subtítulo ---
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src="data:image/png;base64,{logo_base64}" width="150" style="margin-bottom: 1px;" />
            <h2 style='margin-top: 0;'>ABU - Asistente de Bienestar Único</h2>
            <p style='font-size:17px;'>❤️ Tu compañero digital pensado para acompañarte todos los días 💙</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Sección de login con título e instrucción en una sola línea (accesible y compacto) ---
    st.markdown("---")
    st.markdown(
        """
        <h4 style='display: inline;'>🔐 Iniciar sesión:</h4>
        <span style='font-size:17px; margin-left: 5px;'>Seleccioná tu perfil o ingresá como nuevo usuario.</span>
        """,
        unsafe_allow_html=True
    )

    # --- Selector de usuario: perfiles precargados o creación de uno nuevo ---
    perfiles_disponibles = ["(+) Añadir Usuario", "Rosa", "Pedro", "Juan"]
    perfil_seleccionado = st.selectbox("👤 Usuario", perfiles_disponibles)

    # --- Campo de contraseña (oculto al escribir) ---
    password = st.text_input("🔑 Contraseña", type="password", placeholder="Ingresá la clave")

    # --- Botón de acción para iniciar sesión ---
    if st.button("Iniciar sesión"):

        # Validación de clave (muy básica por ahora)
        if password != CLAVE_SECRETA:
            st.error("⚠️ Contraseña incorrecta.")
            return

        # --- Caso: se elige crear un nuevo usuario ---
        if perfil_seleccionado == "(+) Añadir Usuario":
            st.session_state["modo_nuevo_usuario"] = True  # Activa el modo formulario de alta
            st.success("✔️ Acceso como nuevo usuario.")
            st.rerun()

        # --- Caso: se elige un usuario existente ---
        else:
            perfil_key = perfil_seleccionado.lower()       # Se usa como clave interna (en minúsculas)
            datos = obtener_perfil(perfil_key)             # Busca el perfil cargado

            if datos:
                # Carga todos los datos del perfil en session_state para mantenerlos activos durante la sesión
                st.session_state["nombre"] = datos["nombre"]
                st.session_state["edad"] = datos["edad"]
                st.session_state["provincia"] = datos["provincia"]
                st.session_state["descripcion"] = datos["descripcion"]
                st.session_state["vive_solo"] = datos["vive_solo"]
                st.session_state["dificultades"] = datos["dificultades"]
                st.session_state["estado_emocional"] = datos["estado_emocional"]
                st.session_state["preferencias"] = datos["preferencias"]
                st.session_state["contacto_emergencia"] = datos["contacto_emergencia"]
                st.session_state["obra_social"] = datos["obra_social"]
                st.session_state["config_extra_completada"] = True  # Indica que el perfil ya está listo
                st.session_state["modo_nuevo_usuario"] = False      # No es un nuevo usuario

                # Carga opcional de recordatorios si existen
                st.session_state["recordatorios"] = datos.get("recordatorios", [])

                # Mensaje de bienvenida
                st.success(f"¡Bienvenido/a {datos['nombre']}! 💜")
                st.rerun()
            else:
                st.error("No se pudo cargar el perfil. Verificá el nombre.")