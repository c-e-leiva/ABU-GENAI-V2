# app.py
# Módulo principal de la aplicación que integra todas las funcionalidades y módulos.
# Sirve como punto de entrada donde se gestionan las diferentes secciones de la aplicación, como "Conversación", "Noticias", "Ayuda", entre otras.
# Utiliza `Streamlit` para crear la interfaz de usuario y organiza las diferentes opciones que pueden ser seleccionadas por el usuario.
# Este archivo es responsable de inicializar la aplicación y facilitar la interacción entre el usuario y los distintos módulos.

import streamlit as st
from PIL import Image
import os
from recordatorio import mostrar_recordatorios
from conversacion import iniciar_conversacion
from noticias import mostrar_noticias
from ayuda import mostrar_ayuda
from openai import OpenAI

# Cargar claves desde secrets (Streamlit Cloud)
api_key = st.secrets["OPENAI_API_KEY"]
openweather_api_key = st.secrets["OPENWEATHER_API_KEY"]

# Crear instancia del cliente OpenAI
client = OpenAI(api_key=api_key)

# --- Configuración de la página ---
st.set_page_config(page_title="ABU - Asistente de Bienestar Universal", layout="centered")
logo = Image.open("IMG/LOGO.png")  # logo de ABU

# Mostrar logo y título
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=120)
with col2:
    st.markdown("<h2 style='text-align: center; margin-top: 2px;'>ABU - Asistente de Bienestar Único</h2>", unsafe_allow_html=True)

# --- Formulario inicial ---
if "nombre" not in st.session_state:
    with st.form("form_datos_usuario"):
        st.markdown("<h4 style='text-align: center;'>👋 ¡Bienvenido! Contame un poco sobre vos:</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            nombre = st.text_input("Nombre", placeholder="Ej: Tu nombre, apodo o sobrenombre")
        with col2:
            edad = st.number_input("Edad", min_value=0, max_value=120, step=1)

        provincias = [
            "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", "Entre Ríos", 
            "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", 
            "Río Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", 
            "Santiago del Estero", "Tierra del Fuego", "Tucumán", "Ciudad Autónoma de Buenos Aires"
        ]
        provincia = st.selectbox("Provincia", ["¿En qué provincia vivís?"] + provincias)

        descripcion = st.text_area("Contame brevemente sobre vos", placeholder="Ej: Practico fútbol, escucho rock, soy ingeniero.")
        enviar = st.form_submit_button("Comenzar")

        if enviar:
            if nombre and provincia != "¿En qué provincia vivís?":
                st.session_state.nombre = nombre
                st.session_state.edad = edad
                st.session_state.provincia = provincia
                st.session_state.descripcion = descripcion
                st.success(f"¡Hola {nombre}! Ya podés comenzar a usar ABU. 💜")
                st.rerun()
            else:
                st.warning("Por favor completá los campos obligatorios.")

# --- Menú principal ---
def mostrar_menu_principal():
    nombre = st.session_state.nombre
    provincia = st.session_state.provincia
    edad = st.session_state.edad

    st.markdown(f"#### Hola {nombre}, ¿en qué te puedo ayudar hoy? 😊")

    if "opcion" not in st.session_state:
        st.session_state.opcion = None

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🎤 Conversar"):
        st.session_state.opcion = "conversar"
    if col2.button("⏰ Recordatorios"):
        st.session_state.opcion = "recordatorios"
    if col3.button("🌤️ Noticias"):
        st.session_state.opcion = "noticias"
    if col4.button("❗ Ayuda"):
        st.session_state.opcion = "ayuda"

    st.markdown("---")

    if st.session_state.opcion == "conversar":
        iniciar_conversacion("Conversar", nombre, edad, provincia, client)
    elif st.session_state.opcion == "recordatorios":
        mostrar_recordatorios("Recordatorios")
    elif st.session_state.opcion == "noticias":
        mostrar_noticias("Noticias", provincia, openweather_api_key)
    elif st.session_state.opcion == "ayuda":
        mostrar_ayuda("Ayuda", nombre)

if "nombre" in st.session_state:
    mostrar_menu_principal()

st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 15px; color: gray;'>ABU © 2025 - Proyecto en desarrollo por Carlos Ezequiel Leiva. Todos los derechos reservados. | <a href='https://www.linkedin.com/in/c-e-leiva' target='_blank' style='color: gray;'>Mi LinkedIn</a></p>",
    unsafe_allow_html=True
)
