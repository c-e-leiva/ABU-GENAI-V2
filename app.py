# app.py
# Módulo principal de la aplicación que integra todas las funcionalidades y módulos.

# --- Librerías principales ---
import streamlit as st  # Librería principal para la interfaz web
from PIL import Image    # Manejo de imágenes

# --- Módulos de funcionalidades (features) ---
from features.recordatorio import mostrar_recordatorios
from features.conversacion import iniciar_conversacion
from features.noticias import mostrar_noticias
from features.emergencia import mostrar_emergencia
from features.configuracion import mostrar_configuracion

# --- Módulos del núcleo del sistema (core) ---
from storage.perfil_usuario import construir_perfil_usuario, exportar_perfil_completo
from users.estado_emocional import seleccionar_estado_emocional
from core.openai_service import OpenAI  # Cliente para interactuar con la API de OpenAI

# --- Módulo de autenticación de usuario ---
from access.login import mostrar_login


# --- Inicio de sesión o registro de nuevo usuario ---
if "nombre" not in st.session_state and not st.session_state.get("modo_nuevo_usuario", False):
    mostrar_login()
    st.stop()


# --- Cargar claves de acceso desde Streamlit Secrets ---
api_key = st.secrets["OPENAI_API_KEY"]
openweather_api_key = st.secrets["OPENWEATHER_API_KEY"]

# Crear cliente de OpenAI
client = OpenAI(api_key=api_key)


# --- Configuración visual de la aplicación ---
st.set_page_config(page_title="ABU - Asistente de Bienestar Universal", layout="centered")
logo = Image.open("assets/img/logo.png")

# Mostrar logo y título de la app
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=120)
with col2:
    st.markdown("<h2 style='text-align: center; margin-top: 2px;'>ABU - Asistente de Bienestar Único</h2>", unsafe_allow_html=True)


# --- Formulario de registro inicial del usuario ---
if "nombre" not in st.session_state:
    with st.form("form_datos_usuario"):
        st.markdown("<h4 style='text-align: center;'>👋 ¡Bienvenido! Contame un poco sobre vos:</h4>", unsafe_allow_html=True)
        
        # Datos básicos del usuario
        col1, col2 = st.columns([2, 1])
        with col1:
            nombre = st.text_input("Nombre", placeholder="Ej: Tu nombre, apodo o sobrenombre")
        with col2:
            edad = st.number_input("Edad", min_value=0, max_value=120, step=1)

        # Selección de provincia
        provincias = ["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", "Entre Ríos",
                      "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén",
                      "Río Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe",
                      "Santiago del Estero", "Tierra del Fuego", "Tucumán", "Ciudad Autónoma de Buenos Aires"]
        provincia = st.selectbox("Provincia", ["¿En qué provincia vivís?"] + provincias)

        # Descripción personal y situación de vivienda
        descripcion = st.text_area("Contame brevemente sobre vos", placeholder="Ej: Practico fútbol, escucho rock, soy ingeniero.")
        vive_solo = st.radio("¿Vivís solo/a?", ["Sí", "No"], horizontal=True)

        # Preferencias o necesidades especiales
        st.markdown("#### 🧠 ¿Querés que ABU tenga en cuenta alguna dificultad tuya?")
        dificultades = {
            "memoria": st.checkbox("Tengo problemas de memoria"),
            "vision": st.checkbox("Veo con dificultad"),
            "audicion": st.checkbox("Me cuesta escuchar"),
            "movilidad": st.checkbox("Me cuesta moverme con facilidad"),
            "comprension": st.checkbox("A veces me cuesta comprender instrucciones")
        }

        # Servicios deseados
        st.markdown("#### 📅 ¿Querés que te acompañe todos los días con...?")

        noticias = st.checkbox("📰 Noticias del día")
        clima = st.checkbox("🌦️ Clima diario")
        recordatorios = st.checkbox("⏰ Recordatorios personales")

        # Enviar formulario
        enviar = st.form_submit_button("Comenzar")

        # Validación de datos
        if enviar:
            if nombre and provincia != "¿En qué provincia vivís?":
                st.session_state.nombre = nombre
                st.session_state.edad = edad
                st.session_state.provincia = provincia
                st.session_state.descripcion = descripcion
                st.session_state.vive_solo = vive_solo
                st.session_state.dificultades = dificultades
                st.session_state.preferencias = {
                    "noticias": noticias,
                    "clima": clima,
                    "recordatorios": recordatorios
                }
                st.session_state.config_extra_completada = False
                st.success(f"¡Hola {nombre}! Ya podés comenzar a usar ABU. 💜")
                st.rerun()
            else:
                st.warning("Por favor completá los campos obligatorios.")


# --- Configuración adicional posterior al registro ---
if "nombre" in st.session_state and not st.session_state.get("config_extra_completada", False):
    st.markdown("### ⚙️ Configuración adicional (opcional)")

    # Contacto de emergencia
    with st.expander("📞 Registrar contacto de emergencia"):
        agregar_contacto = st.checkbox("Activar contacto de emergencia", key="check_contacto")
        if st.session_state.get("check_contacto"):
            contacto_nombre = st.text_input("Nombre del contacto", key="nombre_contacto")
            contacto_numero = st.text_input("Número de teléfono", key="numero_contacto")
            contacto_relacion = st.selectbox("Relación", ["Familiar", "Amigx", "Pareja", "Hijx", "Otro"], key="relacion_contacto")
            st.session_state.contacto_emergencia = {
                "nombre": contacto_nombre,
                "numero": contacto_numero,
                "relacion": contacto_relacion
            }

    # Obra social o prepaga
    with st.expander("🏥 Registrar obra social o prepaga"):
        tiene_obra_social = st.checkbox("Activar registro de obra social", key="check_obra")
        if st.session_state.get("check_obra"):
            obra_social = st.text_input("Nombre de la obra social", key="nombre_obra")
            telefono_obra_social = st.text_input("Teléfono de contacto", key="telefono_obra")
            st.session_state.obra_social = {
                "nombre": obra_social,
                "telefono": telefono_obra_social
            }

    # Botón para finalizar configuración
    if st.button("Finalizar configuración"):
        st.session_state.config_extra_completada = True
        st.success("¡Datos adicionales guardados con éxito! 😊")
        st.rerun()


# --- Función para mostrar el menú principal de opciones ---
def mostrar_menu_principal():
    perfil_usuario = construir_perfil_usuario(st.session_state)  # Perfil completo construido desde estado
    nombre = perfil_usuario["nombre"]
    provincia = perfil_usuario["provincia"]
    edad = perfil_usuario["edad"]

    st.markdown(f"#### Hola {nombre}, ¿en qué te puedo ayudar hoy? 😊")

    if "opcion" not in st.session_state:
        st.session_state.opcion = None

    # Botones principales del menú
    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("🎤 Conversar"):
        st.session_state.opcion = "conversar"
    if col2.button("⏰ Agenda"):
        st.session_state.opcion = "recordatorios"
    if col3.button("🌤️ Noticias"):
        st.session_state.opcion = "noticias"
    if col4.button("❗ Emergencia"):
        st.session_state.opcion = "emergencia"
    if col5.button("⚙️"):
        st.session_state.opcion = "configuracion"

    st.markdown("---")

    # Ejecutar la funcionalidad correspondiente según la opción seleccionada
    if st.session_state.opcion == "conversar":
        iniciar_conversacion("Conversar", perfil_usuario, client, openweather_api_key=openweather_api_key)
    elif st.session_state.opcion == "recordatorios":
        mostrar_recordatorios("Recordatorios")
    elif st.session_state.opcion == "noticias":
        mostrar_noticias("Noticias", provincia, openweather_api_key)
    elif st.session_state.opcion == "emergencia":
        mostrar_emergencia("Emergencia", nombre)
    elif st.session_state.opcion == "configuracion":
        from features.configuracion import mostrar_configuracion
        datos_completos = exportar_perfil_completo(st.session_state)
        mostrar_configuracion(datos_completos)


# --- Lógica de control del flujo principal ---
if "nombre" in st.session_state and st.session_state.get("config_extra_completada", False):
    if st.session_state.get("estado_emocional") is None:
        seleccionar_estado_emocional()  # Si aún no fue elegido, preguntar cómo se siente
    else:
        mostrar_menu_principal()        # Si ya se eligió, mostrar opciones del asistente


# --- Pie de página de la aplicación ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 15px; color: gray;'>ABU © 2025 - Desarrollado por Carlos Ezequiel Leiva. Todos los derechos reservados. | <a href='https://www.linkedin.com/in/c-e-leiva' target='_blank' style='color: gray;'>Mi LinkedIn</a></p>",
    unsafe_allow_html=True
)
