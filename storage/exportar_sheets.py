# exportar_sheets.py
# Módulo encargado de conectar con Google Sheets y exportar los datos del usuario:
# perfil, recordatorios, contactos de emergencia, historial de conversación y resumen.

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from google.oauth2.service_account import Credentials
import uuid
import streamlit as st


# Definición del alcance de acceso para Google Sheets y credenciales
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Establece la conexión con Google Sheets usando las credenciales del proyecto
def conectar_sheets():
    creds = Credentials.from_service_account_info(dict(st.secrets["gcp_sheets"]), scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

# Obtiene una hoja existente o la crea si no existe
def obtener_hoja(client, spreadsheet_id, nombre_hoja):
    sh = client.open_by_key(spreadsheet_id)
    try:
        worksheet = sh.worksheet(nombre_hoja)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=nombre_hoja, rows="1000", cols="20")
    return worksheet

# Genera un identificador único para el usuario
def generar_id_unico():
    return str(uuid.uuid4())

# Exporta los datos del perfil del usuario a la hoja "Perfil"
def exportar_perfil(spreadsheet_id, datos, client=None):
    if client is None:
        client = conectar_sheets()
    ws = obtener_hoja(client, spreadsheet_id, "Perfil")

    perfil = datos.get("perfil", {})
    id_usuario = perfil.get("nombre", "") + "-" + datetime.now().strftime("%Y%m%d%H%M%S")

    fila = [
        id_usuario,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        perfil.get("nombre", ""),
        perfil.get("edad", ""),
        perfil.get("provincia", ""),
        perfil.get("descripcion", ""),
        perfil.get("vive_solo", ""),
        ", ".join(perfil.get("dificultades", [])),
        perfil.get("estado_emocional", ""),
        ", ".join([k for k, v in perfil.get("preferencias", {}).items() if v])
    ]

    if ws.row_count == 0 or ws.get_all_values() == []:
        encabezado = ["ID", "FechaHora", "Nombre", "Edad", "Provincia", "Descripción", "Vive Solo", "Dificultades", "Estado Emocional", "Preferencias"]
        ws.append_row(encabezado)

    ws.append_row(fila)
    return id_usuario

# Exporta los recordatorios del usuario a la hoja "Recordatorios"
def exportar_recordatorios(spreadsheet_id, datos, id_usuario, client=None):
    if client is None:
        client = conectar_sheets()
    ws = obtener_hoja(client, spreadsheet_id, "Recordatorios")

    recordatorios = datos.get("recordatorios", [])

    if ws.row_count == 0 or ws.get_all_values() == []:
        encabezado = ["ID", "FechaHora Export", "Fecha Recordatorio", "Hora", "Descripción"]
        ws.append_row(encabezado)

    for r in recordatorios:
        fila = [
            id_usuario,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            r.get("fecha", ""),
            r.get("hora", ""),
            r.get("descripcion", ""),
        ]
        ws.append_row(fila)

# Exporta los datos de emergencia (contacto y obra social) a la hoja "Emergencia"
def exportar_emergencia(spreadsheet_id, datos, id_usuario, client=None):
    if client is None:
        client = conectar_sheets()
    ws = obtener_hoja(client, spreadsheet_id, "Emergencia")

    emergencia = datos.get("emergencia", {})
    contacto = emergencia.get("contacto_emergencia", {})
    obra_social = emergencia.get("obra_social", {})

    if ws.row_count == 0 or ws.get_all_values() == []:
        encabezado = ["ID", "FechaHora Export", "Contacto Nombre", "Número", "Relación", "Obra Social Nombre", "Obra Social Teléfono"]
        ws.append_row(encabezado)

    fila = [
        id_usuario,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        contacto.get("nombre", ""),
        contacto.get("numero", ""),
        contacto.get("relacion", ""),
        obra_social.get("nombre", ""),
        obra_social.get("telefono", ""),
    ]
    ws.append_row(fila)

# Exporta el historial de conversación a la hoja "Historial"
def exportar_historial(spreadsheet_id, datos, id_usuario, client=None):
    if client is None:
        client = conectar_sheets()
    ws = obtener_hoja(client, spreadsheet_id, "Historial")

    historial = datos.get("historial", [])

    if ws.row_count == 0 or ws.get_all_values() == []:
        encabezado = ["ID", "Fecha", "Hora", "Rol", "Mensaje"]
        ws.append_row(encabezado)

    for m in historial:
        fecha_hora = datetime.now()
        fila = [
            id_usuario,
            fecha_hora.strftime("%Y-%m-%d"),
            fecha_hora.strftime("%H:%M:%S"),
            m.get("role", ""),
            m.get("content", "")
        ]
        ws.append_row(fila)

# Exporta el resumen de conversación a la hoja "resumen_conversacion"
def exportar_resumen(spreadsheet_id, resumen, id_usuario, client=None):
    if client is None:
        client = conectar_sheets()
    ws = obtener_hoja(client, spreadsheet_id, "resumen_conversacion")

    if ws.get_all_values() == []:
        encabezado = ["ID", "Fecha", "Hora", "Resumen"]
        ws.append_row(encabezado)

    fecha_hora = datetime.now()
    fila = [
        id_usuario,
        fecha_hora.strftime("%Y-%m-%d"),
        fecha_hora.strftime("%H:%M:%S"),
        resumen.strip() if resumen and resumen.strip() else "Todavía no hay suficiente historial para generar un resumen."
    ]
    ws.append_row(fila)

def exportar_todo(spreadsheet_id, datos):
    client = conectar_sheets()
    id_usuario = exportar_perfil(spreadsheet_id, datos, client)
    exportar_recordatorios(spreadsheet_id, datos, id_usuario, client)
    exportar_emergencia(spreadsheet_id, datos, id_usuario, client)
    exportar_historial(spreadsheet_id, datos, id_usuario, client)
    resumen = datos.get("resumen", "")
    exportar_resumen(spreadsheet_id, resumen, id_usuario, client)
    return id_usuario