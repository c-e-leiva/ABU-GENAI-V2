# 🎛️ Gestión de Estado y UI Reactiva

ABU v2 utiliza Streamlit como interfaz principal. Para lograr una experiencia conversacional fluida, sin recargas innecesarias, se hace un uso intensivo de `st.session_state`, el mecanismo de memoria local provisto por Streamlit.

---

## 🧠 ¿Qué es `st.session_state`?

`st.session_state` es un objeto que permite almacenar variables que **persisten entre interacciones** del usuario dentro de una misma sesión. Es esencial para apps interactivas como ABU, donde el estado emocional, el historial y las acciones deben mantenerse entre mensajes.

---

## 🧩 Variables gestionadas en `session_state`

| Variable                     | Propósito                                                            |
|-----------------------------|----------------------------------------------------------------------|
| `perfil_usuario`            | Guarda los datos del usuario (edad, provincia, dificultades, etc.)  |
| `estado_emocional`          | Define el tono y la empatía de las respuestas                        |
| `historial_conversacion`    | Guarda los mensajes del usuario y del asistente                     |
| `modo_emergencia`           | Indica si se activó una situación crítica                           |
| `audio_generado`            | Controla la reproducción del último audio (TTS)                     |
| `respuesta_actual`          | Último mensaje generado por el asistente                            |
| `modo_voz`                  | Indica si la entrada se realiza por voz                             |
| `conversacion_resumida`     | Versión sintetizada para enviar a Google Sheets o mostrar al usuario |

Estas variables son accesibles y modificables desde cualquier parte de la app durante la ejecución.

---

## ⚙️ Ventajas de la gestión de estado

- Evita pérdida de datos entre mensajes.
- Mejora la fluidez de la conversación sin recargar toda la interfaz.
- Permite interacciones complejas (ej. confirmar envío de emergencia).
- Facilita la integración con múltiples componentes (voz, clima, noticias...).

---

## 🖼️ Ejemplo de uso en código

```
import streamlit as st

if "perfil_usuario" not in st.session_state:
    st.session_state.perfil_usuario = {
        "nombre": "Rosa",
        "edad": 72,
        "provincia": "Santa Fe"
    }

st.write(f"Hola {st.session_state.perfil_usuario['nombre']} 👋")
```
---

## 🎯 Consideraciones clave

- `session_state` **se reinicia** si el navegador se cierra o se recarga.
- **No debe usarse** para almacenar datos persistentes entre sesiones (para eso se utiliza Google Sheets o, a futuro, una base de datos real).
- Puede usarse para **bloquear funciones temporales**, como:
  - Evitar repetir una alerta de emergencia.
  - Controlar si un audio ya fue generado o reproducido.
  - Restringir accesos condicionales en la interfaz.

---

## 🔮 Futuras mejoras

- **Persistencia selectiva** del estado entre sesiones, usando:
  - Google Firestore
  - IndexedDB (almacenamiento local del navegador)
- **Panel editable de configuración** del usuario basado en los valores actuales de `session_state`.
- Sincronización entre estado emocional y respuestas previas para análisis longitudinal.

---

> 🧪 Esta sección es clave para mantener una experiencia fluida, reactiva y accesible, especialmente pensada para personas mayores o con dificultades cognitivas. El manejo del estado interno es fundamental para un asistente que acompaña de forma continua y empática.
