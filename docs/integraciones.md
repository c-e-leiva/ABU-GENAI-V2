# 🌐 Integraciones Externas

ABU v2 se apoya en diversas APIs y servicios externos para enriquecer la interacción con el usuario, brindar información útil en tiempo real y facilitar la entrada/salida por voz. Esta sección describe cada integración y su propósito dentro del sistema.

---

## 🔮 Modelos de lenguaje (OpenAI)

| Servicio            | Uso principal                             | Módulo asociado              |
|---------------------|--------------------------------------------|------------------------------|
| **GPT-4 Turbo**     | Conversación principal empática            | `core/openai_service.py`     |
| **GPT-3.5 Turbo**   | Resúmenes, tareas deterministas, pruebas   | `storage/resumen_historial.py` |

- Ambos modelos se llaman usando la API de OpenAI.
- Se utiliza la arquitectura de *chat completion* (`chat/completions`).
- Se intercambian según contexto y objetivo del mensaje.

---

## 🗣️ Voz (Texto a Voz y Voz a Texto)

| Servicio                         | Función                        | Módulo asociado       |
|----------------------------------|--------------------------------|------------------------|
| **Google Cloud Text-to-Speech** | Conversión de texto a voz natural | `services/tts.py`   |
| **Streamlit Mic Recorder**      | Grabación y envío de voz desde la UI | `services/stt.py`   |
| **Speech-to-Text** (Google o local) | Conversión de voz a texto      | `services/stt.py`     |

- Se utilizan voces naturales, configurables por idioma, tono y velocidad.
- La grabación se maneja desde la interfaz usando un componente personalizado de Streamlit.
- Puede integrarse con Whisper u otras herramientas si se desea usar STT local.

---

## 📰 Información en tiempo real

| Servicio          | Función                      | Módulo asociado           |
|-------------------|-------------------------------|---------------------------|
| **OpenWeather API** | Consulta de clima actual     | `features/noticias.py`    |
| **Clarín RSS**    | Noticias nacionales/locales    | `features/noticias.py`    |

- El clima se adapta según la provincia del usuario.
- Las noticias se obtienen desde un feed RSS, por defecto de Clarín (puede configurarse).

---

## 📤 Exportación y almacenamiento inicial

| Servicio               | Uso                                 | Módulo asociado             |
|------------------------|--------------------------------------|------------------------------|
| **Google Sheets API**  | Exportar perfil y resumen conversacional | `storage/exportar_sheets.py` |

- El perfil del usuario y un resumen afectivo de la conversación se exportan a una hoja de cálculo de Google Drive.
- Esto permite análisis, seguimiento y visualización externa sin necesidad de una base de datos al inicio.

---

## 🔐 Credenciales y seguridad

- Todas las claves API se almacenan localmente en:
  - El archivo `.env` (variables de entorno)
  - La carpeta `credentials/` (archivos `.json` de Google Cloud)
- Estos archivos están incluidos en `.gitignore` y **no se suben al repositorio público**.
- En producción, se recomienda el uso de **Google Secret Manager**, Vault o `.env` cifrados.

---

## 🧩 Resumen de módulos involucrados

| Integración                  | Archivo                             |
|-----------------------------|--------------------------------------|
| OpenAI API                  | `core/openai_service.py`             |
| Google TTS (voz salida)     | `services/tts.py`                    |
| STT / Mic Recorder (voz entrada) | `services/stt.py`               |
| OpenWeather + Clarín RSS    | `features/noticias.py`               |
| Exportación a Google Sheets | `storage/exportar_sheets.py`         |
| Resumen conversacional      | `storage/resumen_historial.py`       |

---

> 📌 Estas integraciones permiten a ABU brindar una experiencia rica, adaptativa y centrada en el usuario, sin requerir infraestructura compleja en su versión inicial.