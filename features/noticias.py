# noticias.py
# Módulo encargado de mostrar noticias y clima dentro de la aplicación.
# Se conecta a OpenWeather API para datos meteorológicos y a un feed RSS para titulares diarios.

import streamlit as st
import requests
import feedparser
from datetime import datetime

# Diccionario de días en español para traducción
DIAS_ESP = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves",
    "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}

# Obtiene el clima actual de una provincia usando la API de OpenWeather
def obtener_clima(provincia, openweather_api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={provincia}&appid={openweather_api_key}&units=metric&lang=es"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        descripcion = data["weather"][0]["description"]
        temperatura = data["main"]["temp"]
        return descripcion, temperatura
    return None, None

# Obtiene el pronóstico extendido para los próximos días (5 días, cada 3 hs)
def obtener_pronostico(provincia, openweather_api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={provincia}&appid={openweather_api_key}&units=metric&lang=es"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Muestra la sección de noticias y clima dentro de la interfaz de usuario
def mostrar_noticias(seleccion, provincia, openweather_api_key):
    if seleccion != "Noticias":
        return

    st.markdown("#### 🌤️ Clima de hoy")

    ahora = datetime.now()
    dia_actual_esp = DIAS_ESP.get(ahora.strftime("%A"), ahora.strftime("%A"))
    hora_actual = ahora.strftime("%H:%M")

    # Mostrar clima actual
    clima, temperatura = obtener_clima(provincia, openweather_api_key)
    if clima and temperatura is not None:
        st.info(f"🌡️ **Clima actual:** {dia_actual_esp}, {hora_actual} hs. **{round(temperatura)}°C**, {clima} en {provincia}")
    else:
        st.error("⚠️ No se pudo obtener el clima actual.")

    # Mostrar pronóstico para los próximos 2 días
    st.markdown("##### 📆 Pronóstico para los próximos 2 días:")
    datos_forecast = obtener_pronostico(provincia, openweather_api_key)
    if datos_forecast:
        dias_mostrados = set()
        contador = 0
        for entrada in datos_forecast["list"]:
            fecha = datetime.strptime(entrada["dt_txt"], "%Y-%m-%d %H:%M:%S")
            if fecha.date() > ahora.date():
                clave_dia = fecha.strftime("%A %d/%m")
                if clave_dia not in dias_mostrados:
                    dia_esp = DIAS_ESP.get(fecha.strftime("%A"), fecha.strftime("%A"))
                    temp = round(entrada["main"]["temp"])
                    desc = entrada["weather"][0]["description"]
                    st.markdown(f"📅 {dia_esp} {fecha.strftime('%d/%m')}: {temp}°C, {desc}")
                    dias_mostrados.add(clave_dia)
                    contador += 1
                if contador == 2:
                    break
    else:
        st.warning("⚠️ No se pudo obtener el pronóstico extendido.")

    st.markdown("---")
    # Mostrar titulares de noticias
    st.markdown("#### 📰 Titulares de hoy")
    rss_url = "https://www.clarin.com/rss/"
    noticias = feedparser.parse(rss_url)
    for noticia in noticias.entries[:5]:
        st.markdown(f"🔹 [{noticia.title}]({noticia.link})")

# Devuelve un resumen textual del clima para el asistente
def obtener_texto_clima(provincia, openweather_api_key):
    descripcion, temperatura = obtener_clima(provincia, openweather_api_key)
    if descripcion and temperatura is not None:
        ahora = datetime.now()
        dia_actual_esp = DIAS_ESP.get(ahora.strftime("%A"), ahora.strftime("%A"))
        hora_actual = ahora.strftime("%H:%M")
        return (f"Hoy es {dia_actual_esp} y son las {hora_actual}. "
                f"En {provincia} el clima está {descripcion}, con una temperatura de aproximadamente {round(temperatura)}°C.")
    else:
        return "Lo siento, no pude obtener el clima en este momento."

# Devuelve un resumen textual con los principales titulares de noticias
def obtener_texto_noticias():
    rss_url = "https://www.clarin.com/rss/"
    noticias = feedparser.parse(rss_url)
    titulares = noticias.entries[:3]
    if titulares:
        texto = "Aquí tenés los titulares principales de hoy:\n\n"
        for noticia in titulares:
            texto += f"• {noticia.title.strip()}. \n"
        return texto.strip()
    return "No pude obtener las noticias en este momento."

# Detecta si el mensaje del usuario se refiere a clima, noticias o recordatorios
def detectar_intencion_extra(mensaje: str) -> str:
    mensaje = mensaje.lower()
    if any(palabra in mensaje for palabra in ["clima", "temperatura", "pronóstico", "calor", "frío"]):
        return "clima"
    elif any(palabra in mensaje for palabra in ["noticias","noticia", "titulares","titular"]):
        return "noticias"
    elif any(palabra in mensaje for palabra in ["recordatorio", "recordatorios", "agenda", "agendas", "agenda diaria", "agenda personal"]):
        return "recordatorios"
    else:
        return "ninguna"
