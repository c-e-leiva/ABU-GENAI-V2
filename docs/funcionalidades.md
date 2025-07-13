# ⚙️ Flujo de Usuario y Funcionalidades

Esta sección detalla cómo interactúa el usuario con ABU, desde el primer acceso hasta las funcionalidades principales del asistente, con foco en la experiencia empática, adaptativa y personalizada.

---

## 🧾 Flujo General de Interacción

1. **Acceso inicial**: el usuario ingresa desde un navegador web a la app desarrollada en Streamlit.
2. **Login / Inicio de sesión** *(opcional según configuración)*.
3. **Carga del perfil**: nombre, edad, provincia, si vive solo, dificultades, preferencias.
4. **Estado emocional**: el usuario selecciona un emoji que representa cómo se siente (feliz, pensante, triste, ansioso, etc.).
5. **Interacción libre**:
   - Puede escribir o hablar.
   - El sistema analiza la intención, el contexto y el estado emocional.
   - Se genera una respuesta adaptada, que puede reproducirse en voz si el usuario lo desea.

---

## 💡 Funcionalidades principales

### 🗣️ 1. Conversación empática

- ABU adapta su tono y contenido según el estado emocional detectado.
- Usa GPT-4 Turbo con instrucciones personalizadas (via `prompt_manager.py`).
- Mantiene el contexto a lo largo de la charla con ayuda de LangChain.

### 🕒 2. Recordatorios y agenda

- El usuario puede pedir que ABU le recuerde:
  - Tomar medicación
  - Llamar a alguien
  - Hacer una tarea a cierta hora
- Los datos se almacenan localmente y/o exportan a Google Sheets.
- Se puede consultar, eliminar o actualizar cada recordatorio.

### 🌤️ 3. Clima y noticias locales

- ABU obtiene la ubicación del usuario (por provincia configurada).
- Consulta el clima actual usando **OpenWeather API**.
- Accede a titulares del día mediante RSS de medios como Clarín.

### 🚨 4. Emergencia asistida

- Si el usuario expresa frases como *“necesito ayuda”*, *“me siento mal”* o *“llamá a alguien”*, ABU activa el protocolo de emergencia.
- Se envía un mensaje (simulado en demo) a un contacto de confianza.
- Se incluye la ubicación, el motivo y el nombre del usuario.
- Se reproduce un mensaje de contención mientras llega la ayuda.

### ⚙️ 5. Configuración del perfil

Actualmente, el perfil del usuario se configura al inicio de la interacción (nombre, edad, provincia, dificultades, etc.), y se mantiene durante la sesión activa.

📝 **Funcionalidades previstas** (aún no implementadas):

- Actualizar datos personales luego del inicio.
- Cambiar preferencias (tema de conversación, tipo de voz).
- Editar contactos de emergencia o ubicación.

Estas opciones están contempladas en el diseño del sistema y serán integradas en versiones futuras para permitir una personalización más flexible y persistente.


---

## 🎙️ Entrada y salida por voz

- Entrada por voz: mediante el componente `Streamlit Mic Recorder`, convertido por `services/stt.py`.
- Salida en voz natural: con **Google Cloud Text-to-Speech** (configurable por idioma, voz y velocidad).

---

## 🧩 Módulos involucrados

| Funcionalidad         | Archivo principal                    |
|-----------------------|--------------------------------------|
| Conversación          | `features/conversacion.py`           |
| Recordatorios         | `features/recordatorio.py`           |
| Noticias y clima      | `features/noticias.py`               |
| Emergencia            | `features/emergencia.py`             |
| Configuración         | `features/configuracion.py`          |
| Análisis emocional    | `users/estado_emocional.py`          |

---

## 🧠 Personalización dinámica

Gracias a la combinación del perfil cargado, el estado emocional y la memoria contextual, ABU:

- Usa diferentes tonos y palabras según cómo se siente el usuario.
- Detecta cuándo un mensaje requiere una acción (alerta, contención, sugerencia).
- Ofrece contenido útil y cálido, con un enfoque humano y empático.

---

> 🧪 Esta sección forma parte del diseño centrado en el usuario (UX conversacional), clave para el impacto real del proyecto.