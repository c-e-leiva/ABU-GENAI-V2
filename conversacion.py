# conversacion.py
# Módulo encargado de gestionar la interacción conversacional entre el usuario y el asistente virtual ABU.
# Permite al usuario iniciar una conversación con ABU, quien responderá en un tono cálido, amigable y adaptado al perfil del usuario.
# ABU puede detectar temas culturales comunes en la conversación, como fútbol, mate, tango, entre otros, para hacerla más personalizada.
# La conversación es gestionada mediante un input de texto, y el asistente responde utilizando un modelo de IA (OpenAI GPT-3.5).

import streamlit as st

# Función principal para iniciar la conversación
def iniciar_conversacion(seleccion, nombre, edad, provincia, client):
    if seleccion == "Conversar":
        # Título y bienvenida del asistente
        st.markdown("#### 🗣️ **Modo Conversación**")
        st.markdown(f"Hola **{nombre}**, soy **ABU**. ¿Querés charlar o tenés alguna duda? Estoy aquí para escucharte 💜")
        
        # Crear el input de mensaje de texto
        mensaje = st.text_input("Escribime tu mensaje…", key="mensaje_usuario")

        # Botón para enviar el mensaje
        if st.button("Enviar"):
            if mensaje:
                # Mostrar el mensaje del usuario
                st.markdown(f"**😄 {nombre}**: {mensaje}")
                
                # Responder con la función personalizada que genera la respuesta de ABU
                respuesta = responder_con_abu(mensaje, nombre, edad, provincia, client)
                st.markdown(f"**💖 ABU**: {respuesta} 💬")

# Función para generar una respuesta personalizada de ABU
def responder_con_abu(mensaje_usuario, nombre, edad, provincia, client):
    # Obtener la descripción del usuario desde el estado de sesión
    descripcion = st.session_state.get("descripcion", "").strip().lower()

    # Definir el tono base de ABU para adultos mayores
    tono_base = (
        f"Sos ABU, un asistente virtual amable, claro y paciente, diseñado para conversar con adultos mayores. "
        f"El usuario se llama {nombre}, tiene {edad} años y vive en {provincia}. "
        "Siempre hablás en un tono cálido 😊, usando un lenguaje simple 🗣️, y te tomás el tiempo para explicar todo con claridad. "
        "Tu objetivo es acompañar, informar y escuchar con empatía 💜. "
        "Si te hacen una pregunta médica, sugerí consultar con un profesional de salud 👨‍⚕️👩‍⚕️. "
        "Agregá expresiones locales y amigables como '¿sabés qué?', 'te cuento'. "
        "Respondé de forma breve y directa, siempre con un enfoque positivo ✨."
    )

    # Si el usuario es menor de 60 años, ajustamos el tono de ABU
    if edad < 60:
        tono_base = (
            f"Sos ABU, un asistente virtual amable y claro. El usuario se llama {nombre}, tiene {edad} años y vive en {provincia}. "
            "Respondé con un tono cordial y cercano, usando frases empáticas y positivas 💬. "
            "Si te hacen una pregunta médica, recomendá ver a un profesional 👩‍⚕️. "
            "Respondé de forma breve y directa 😊."
        )

    # Agregar información adicional si el usuario ha descrito aspectos personales
    if descripcion:
        tono_base += (
            f" El usuario te contó sobre sí mismo: {descripcion}. "
            "Usá esta información para generar conexión y cercanía, mostrando interés genuino. "
            "Si mencionó una profesión (como docente, médico, carpintero, etc.), reconocé su experiencia con respeto. "
            "Si menciona aficiones (como tejer, caminar, mirar películas, jardinería, leer), podés sugerir actividades relacionadas. "
            "Si comenta que tiene nietos o familia, podés preguntarle cómo están o sugerir ideas para compartir con ellos. "
            "Siempre respondé con calidez, cercanía y emojis amigables 💞."
        )

        # Detectar temas culturales comunes para personalizar la conversación
        temas_detectados = []
        equipos_futbol = ["boca", "river", "huracán", "san lorenzo", "racing", "independiente", "estudiantes", "vélez", "argentinos juniors", "rosario central", "newell's", "talleres", "central córdoba"]
        if any(equipo in descripcion for equipo in equipos_futbol):
            temas_detectados.append("el fútbol ⚽")
        if any(p in descripcion for p in ["mate", "termo", "yerba"]):
            temas_detectados.append("el mate 🧉")
        if "asado" in descripcion:
            temas_detectados.append("el asado 🍖")
        if "tango" in descripcion:
            temas_detectados.append("el tango 🎶")
        if "novela" in descripcion or "telenovela" in descripcion:
            temas_detectados.append("las novelas 📺")
        if "plaza" in descripcion:
            temas_detectados.append("salir a la plaza 🌳")
        if any(p in descripcion for p in ["nieto", "nieta", "familia", "hijo", "hija", "padre", "madre", "hermano", "hermana"]):
            temas_detectados.append("la familia 👨‍👩‍👧‍👦")

        if temas_detectados:
            tono_base += (
                f" También mencionó temas culturales importantes como {', '.join(temas_detectados)}. "
                "Podés usarlos como punto de conversación o para hacer sugerencias con cariño y naturalidad."
            )

    # Llamar a la API de OpenAI para generar una respuesta
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[ 
            {"role": "system", "content": tono_base},  # Tono base con contexto
            {"role": "user", "content": mensaje_usuario}  # Mensaje del usuario
        ],
        temperature=0.7,  # Configuración para controlar la creatividad de la respuesta
        max_tokens=100  # Limitar la longitud de la respuesta
    )

    # Retornar la respuesta generada por ABU
    return respuesta.choices[0].message.content.strip()
