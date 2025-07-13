# 💬 Prompt y Modelos de IA

Esta sección describe cómo se construyen las instrucciones que recibe el modelo de lenguaje (prompt engineering), los modelos utilizados en ABU v2 y cómo se ajustan sus parámetros para lograr una interacción empática y funcional.

---

## 🧠 Prompt Manager

El módulo `core/prompt_manager.py` se encarga de construir un **prompt dinámico** que guía al modelo (GPT-4 o GPT-3.5) para generar respuestas personalizadas y contextuales.

### Componentes del prompt:

- **Perfil del usuario** (nombre, edad, provincia, dificultades, preferencias)
- **Estado emocional** actual (determinante para el tono de respuesta)
- **Historial conversacional resumido** (mediante LangChain)
- **Intención del mensaje del usuario**
- **Instrucciones específicas del sistema y la personalidad del asistente**

El objetivo es generar respuestas cálidas, claras y adaptadas al contexto y necesidad emocional de cada usuario.

---

## 🧪 Modelos de lenguaje utilizados

| Tarea                       | Modelo           | Justificación                                     |
|----------------------------|------------------|--------------------------------------------------|
| Conversación principal     | GPT-4 Turbo      | Alta calidad, respuestas empáticas y coherentes |
| Tareas auxiliares          | GPT-3.5 Turbo    | Resúmenes, tareas específicas con menor costo    |

Los modelos se seleccionan dinámicamente según el tipo de tarea.

---

## 🎛️ Parámetros ajustables

ABU adapta los parámetros del modelo según el tipo de interacción para equilibrar **precisión, creatividad y calidez**.

| Contexto                     | Temperatura | Finalidad                     |
|-----------------------------|-------------|-------------------------------|
| Emergencias / respuestas críticas | 0.2         | Precisión y control            |
| Conversación general         | 0.7         | Naturalidad y empatía         |
| Resúmenes y análisis         | 0.6         | Claridad con algo de flexibilidad |

---

## 🧬 Memoria conversacional

- Implementada en `core/memoria.py` usando **LangChain**.
- Permite mantener el contexto de la conversación entre turnos.
- Mejora la coherencia y la personalización de las respuestas.
- También se usa para detectar situaciones sensibles (módulo `detectar_emergencia.py`).

---

## 📌 Detalles técnicos adicionales

- Se usan roles "system", "user" y "assistant" para estructurar los mensajes enviados a la API.
- El historial del usuario es preprocesado y resumido para evitar sobrepasar el límite de tokens.
- Las respuestas se filtran para ajustar tono y forma antes de ser enviadas por voz (TTS) o texto.

---

> 🧩 Módulos involucrados:  
> `core/prompt_manager.py`  
> `core/openai_service.py`  
> `core/memoria.py`  
> `features/resumen_historial.py`
