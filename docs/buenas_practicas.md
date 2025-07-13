# 🔒 Buenas Prácticas y Seguridad

Esta sección detalla los principios de desarrollo, normas de seguridad y decisiones arquitectónicas aplicadas en ABU v2 para garantizar un proyecto robusto, mantenible y preparado para futuras mejoras.

---

## 🧱 Arquitectura modular

El proyecto sigue una estructura **por capas funcionales**, que separa responsabilidades claramente:

- `core/`: lógica conversacional y generación de prompts  
- `features/`: funcionalidades visibles para el usuario  
- `services/`: entrada/salida de voz  
- `storage/`: persistencia y exportación de datos  
- `users/`: datos de prueba, perfiles y análisis emocional  
- `access/`: login y control de sesión  

Esta modularidad facilita:

- Escalar o reemplazar partes sin afectar otras  
- Mantener y depurar el código fácilmente  
- Incorporar colaboradores sin curva de aprendizaje alta  

---

## ✅ Legibilidad y mantenimiento

- Código limpio y comentado donde es necesario  
- Nombrado semántico de variables, módulos y funciones  
- Archivos `.md` en `/docs/` para guiar a otros desarrolladores  
- Separación clara entre lógica de negocio y capa de presentación (Streamlit)  

---

## 🔐 Seguridad de credenciales

Todas las claves y accesos a servicios externos (APIs de OpenAI, Google Cloud, etc.) están **excluidos del repositorio público**.

### Ubicación de las credenciales:

- `.streamlit/config.toml`: contiene las claves API bajo la sección `[secrets]`  
- `credentials/`: almacena archivos `.json` de Google Cloud (TTS, Sheets)

### Protección del proyecto:

- `config.toml` y `credentials/` están incluidos en `.gitignore`  
- El sistema nunca expone claves en el frontend o en respuestas del asistente  
- Preparado para migrar a un sistema de gestión de secretos (Vault, GCP Secret Manager) en producción  

---

## ⚠️ Manejo de errores

- Captura de excepciones en puntos críticos:
  - Conexiones con APIs externas  
  - Generación de audio  
  - Fallas de red o datos incompletos  

- Mensajes claros y empáticos al usuario ante cualquier error:
  > "Hubo un problemita al conectarme. Probemos de nuevo en unos segundos 😊"

---

## 📈 Escalabilidad futura

El proyecto está preparado para migrar desde una demo local a un entorno productivo más robusto:

- **Almacenamiento**: pasar de Google Sheets a bases de datos como Firestore o PostgreSQL  
- **Backend**: posibilidad de separar frontend (Streamlit) de backend (FastAPI, Flask)  
- **Despliegue en nube**: Dockerización y hosting en GCP, Vercel, Render u otros  
- **IA desacoplada**: orquestación vía eventos o tareas programadas con colas de trabajo  

---

> 🧪 Estas prácticas no solo garantizan un código mantenible, sino que refuerzan la confianza del usuario final en un asistente que maneja datos personales, voz e interacciones emocionales de forma ética y segura.
