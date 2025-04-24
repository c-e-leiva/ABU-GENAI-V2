# noticias.py
# Módulo encargado de mostrar las noticias y el clima en la aplicación.
# Obtiene el clima actual y el pronóstico extendido de una ciudad utilizando la API de OpenWeatherMap.
# Además, muestra titulares de noticias obtenidos de un feed RSS de Clarín.
# Utiliza el módulo `feedparser` para leer el RSS y `requests` para consultar la API de OpenWeatherMap.

import streamlit as st
import requests
import feedparser
from datetime import datetime

# Diccionario de días de la semana en español
DIAS_ESP = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves",
    "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}

# Función para obtener el clima actual
def obtener_clima(provincia, openweather_api_key):
    # URL de la API de OpenWeather para obtener el clima actual
    url = f"http://api.openweathermap.org/data/2.5/weather?q={provincia}&appid={openweather_api_key}&units=metric&lang=es"
    response = requests.get(url)
    if response.status_code == 200:  # Si la respuesta es exitosa
        data = response.json()  # Convertir la respuesta JSON
        descripcion = data["weather"][0]["description"]  # Descripción del clima
        temperatura = data["main"]["temp"]  # Temperatura actual
        return descripcion, temperatura
    return None, None  # Retornar None si hay un error al obtener el clima

# Función para obtener el pronóstico extendido (próximos 5 días)
def obtener_pronostico(provincia, openweather_api_key):
    # URL para obtener el pronóstico extendido
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={provincia}&appid={openweather_api_key}&units=metric&lang=es"
    response = requests.get(url)
    if response.status_code == 200:  # Si la respuesta es exitosa
        return response.json()  # Retornar la respuesta JSON del pronóstico
    return None  # Retornar None si no se pudo obtener el pronóstico

# Función para mostrar las noticias y el clima
def mostrar_noticias(seleccion, provincia, openweather_api_key):
    if seleccion != "Noticias":  # Solo mostrar noticias si se selecciona la opción de noticias
        return

    st.markdown("#### 📰 Noticias")  # Título para la sección de noticias

    ahora = datetime.now()  # Obtener la fecha y hora actual
    dia_actual_esp = DIAS_ESP.get(ahora.strftime("%A"), ahora.strftime("%A"))  # Traducir el día al español
    hora_actual = ahora.strftime("%H:%M")  # Formatear la hora actual

    # Mostrar clima actual
    clima, temperatura = obtener_clima(provincia, openweather_api_key)
    if clima and temperatura is not None:  # Si se pudo obtener el clima
        st.info(f"**Clima actual:** {dia_actual_esp}, {hora_actual} hs. **{round(temperatura)}°C**, {clima} en {provincia}")
    else:
        st.error("⚠️ No se pudo obtener el clima actual.")  # Si no se puede obtener el clima, mostrar un error

    # Pronóstico extendido (para los próximos 2 días)
    st.markdown("##### 📆 Pronóstico para los próximos 2 días:")
    datos_forecast = obtener_pronostico(provincia, openweather_api_key)  # Obtener el pronóstico extendido
    if datos_forecast:
        dias_mostrados = set()  # Para evitar mostrar el mismo día varias veces
        contador = 0  # Contador para mostrar solo 2 días de pronóstico

        # Iterar sobre las entradas del pronóstico
        for entrada in datos_forecast["list"]:
            fecha = datetime.strptime(entrada["dt_txt"], "%Y-%m-%d %H:%M:%S")  # Convertir la fecha a formato datetime
            if fecha.date() > ahora.date():  # Solo mostrar pronósticos futuros
                clave_dia = fecha.strftime("%A %d/%m")  # Formatear la fecha para que no se repita
                if clave_dia not in dias_mostrados:  # Si el día no ha sido mostrado aún
                    dia_esp = DIAS_ESP.get(fecha.strftime("%A"), fecha.strftime("%A"))  # Traducir al español
                    temp = round(entrada["main"]["temp"])  # Redondear la temperatura
                    desc = entrada["weather"][0]["description"]  # Descripción del clima
                    st.markdown(f"📅 {dia_esp} {fecha.strftime('%d/%m')}: {temp}°C, {desc}")  # Mostrar el pronóstico
                    dias_mostrados.add(clave_dia)  # Marcar el día como mostrado
                    contador += 1
                if contador == 2:  # Detenerse después de mostrar 2 días
                    break
    else:
        st.warning("⚠️ No se pudo obtener el pronóstico extendido.")  # Si no se pudo obtener el pronóstico, mostrar advertencia

    # Noticias
    st.markdown("##### 🗞️ Titulares de hoy")
    rss_url = "https://www.clarin.com/rss/"  # URL del RSS de Clarin
    noticias = feedparser.parse(rss_url)  # Parsear el RSS

    # Mostrar las primeras 5 noticias
    for noticia in noticias.entries[:5]:
        st.markdown(f"🔹 [{noticia.title}]({noticia.link})")  # Mostrar cada noticia con su título y enlace
