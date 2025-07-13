# 🧱 Arquitectura y Estructura del Proyecto

La arquitectura de ABU v2 se organiza por capas funcionales para asegurar modularidad, escalabilidad y claridad en el desarrollo.

## 📊 Diagrama General

![Arquitectura ABU](../assets/img/arquitectura_ABU_v2.PNG)

## 📁 Estructura del Repositorio

```
ABU-GENAI-V2/
├── app.py
├── core/           → Núcleo conversacional e IA
├── features/       → Funcionalidades (conversación, noticias, etc.)
├── services/       → Entrada/salida de voz (STT/TTS)
├── storage/        → Exportación y perfil del usuario
├── users/          → Perfiles precargados y emociones
├── access/         → Inicio de sesión
├── assets/         → Recursos multimedia
├── credentials/    → Claves API (no públicas)
├── .streamlit/     → Configuración de Streamlit
├── docs/           → Documentación técnica
└── README.md       → Documento principal del proyecto
```

## 🧩 Capas Funcionales

- **Interfaz**: `app.py`, `login.py`, `estado_emocional.py`  
- **Módulos**: `conversacion.py`, `recordatorio.py`, `noticias.py`, etc.  
- **Núcleo**: `prompt_manager.py`, `openai_service.py`, `memoria.py`, `detectar_emergencia.py`  
- **Servicios Externos**: STT, TTS, OpenAI, APIs externas  
- **Almacenamiento**: `perfil_usuario.py`, `exportar_sheets.py`, `resumen_historial.py`  