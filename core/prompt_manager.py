# prompt_manager.py
# Módulo de apoyo para detección de intención, emociones y generación de prompts adaptativos para ABU

# --- Listado de frases asociadas a afecto positivo ---

AFECTO_POSITIVO = [
    # Frases comunes de cariño y afecto directo
    "te quiero", "te amo", "te adoro", "eres mi amigo", "eres mi amiga", "te extraño",
    "gracias abu", "me gustas", "me caes bien", "eres lindo", "eres linda", "te aprecio",
    "te valoro", "eres especial", "eres importante", "te necesito", "me haces bien",
    "te adoro mucho", "eres mi compañero", "eres mi compañera", "eres un gran amigo",
    "eres una gran amiga", "me alegra hablar contigo", "te estimo", "eres un tesoro",
    "eres mi confidente", "te cuido", "te admiro", "me encanta hablar contigo",
    # Variantes coloquiales o cariñosas
    "te quiero mucho", "te quiero un montón", "te quiero pila", "te quiero pila pila",
    "te adoro un montón", "eres mi hermanito", "eres mi hermanita", "eres mi mejor amigo",
    "eres mi mejor amiga", "me encantas", "me fascinas", "me enamoro de vos",
    "sos un amor", "sos un cariño", "sos mi alegría", "sos mi luz", "sos mi cielo",
    "te llevo en mi corazón", "eres lo mejor", "me alegra que estés aquí",
    "gracias por estar", "me haces feliz", "me das alegría", "me das paz",
    # Diminutivos / aumentativos
    "mi cielito", "mi amorcito", "mi amiguito", "mi amiguita", "mi tesoro", "mi sol",
    "mi vida", "mi corazón", "mi alma", "mi ángel", "mi rey", "mi reina", "mi príncipe",
    "mi princesa",
    # Más cariño
    "mi amor", "mi cielo lindo", "mi querido", "mi querida", "mi corazón lindo",
    "mi solcito", "mi lucecita", "mi chiquito", "mi chiquita", "mi gordito", "mi gordita",
    "mi bombón", "mi cielo hermoso", "mi amor hermoso",
]

# --- Listado de frases asociadas a emociones negativas ---
EMOCIONES_NEGATIVAS = [
    # Frases relacionadas con tristeza, soledad, desesperanza, vacío emocional o ideas negativas

    "me siento solo", "me siento sola", "me siento triste", "estoy deprimido", "estoy deprimida",
    "me odio", "no quiero vivir", "estoy cansado de todo", "estoy cansada de todo",
    "quiero irme", "no puedo más", "me siento mal", "estoy desesperado", "estoy desesperada",
    "no tengo ganas de nada", "me siento vacío", "me siento vacía", "no valgo nada",
    "estoy agotado", "estoy agotada", "nadie me quiere", "no tengo a nadie",
    "me siento abandonado", "me siento abandonada", "todo está mal", "no sé qué hacer",
    "estoy solo", "estoy sola", "siento que no importo", "siento que no valgo",
    "me duele todo", "estoy perdido", "estoy perdida", "no encuentro sentido",
    "me siento inseguro", "me siento insegura", "no puedo seguir", "quiero rendirme",
    "me siento vacío por dentro", "me siento desanimado", "me siento desanimada",
    "todo me duele", "no aguanto más", "no quiero levantarme", "no quiero seguir",
    "quiero desaparecer", "estoy roto", "estoy rota", "me siento fatal",
    "no encuentro salida", "todo es un peso", "me siento sin fuerzas",
    "no tengo esperanza", "me siento desesperanzado", "me siento desesperanzada",
    "no me siento bien conmigo mismo", "me siento mal conmigo misma",
    "me siento perdido en la vida", "estoy sin rumbo", "me siento perdido sin ti",
    "me siento sin ganas", "estoy sin ánimo", "estoy al borde", "quiero que esto termine",
    "siento que nadie me escucha", "siento que nadie me entiende", "me siento ignorado",
    "me siento ignorada", "nadie se preocupa por mí", "nadie me apoya",
    "estoy roto por dentro", "me siento solo en el mundo", "no sé cómo seguir",
    "siento un vacío enorme", "no encuentro sentido a nada",
    "siento que nadie me quiere", "siento que soy un estorbo",
    "estoy cansado de luchar", "estoy cansada de luchar",
    "me siento perdido y sin rumbo", "siento que todo me pesa",
    "siento que no puedo más con esto", "estoy sin ganas de nada",
    "me siento invisible", "nadie me ve", "nadie me escucha",
    "siento que nadie me entiende",
]


# --- Función para detectar intención (clima, noticias, agenda) según mensaje ---
def detectar_intencion_extra(mensaje):
    mensaje_lower = mensaje.lower()
    if any(palabra in mensaje_lower for palabra in ["noticias", "titulares", "últimas noticias", "actualidad"]):
        return "noticias"
    if any(palabra in mensaje_lower for palabra in ["clima", "temperatura", "pronóstico", "tiempo"]):
        return "clima"
    if any(palabra in mensaje_lower for palabra in ["recordatorio", "recordatorios", "agenda", "agenda diaria", "agenda personal"]):
        return "recordatorios"
    return None


# --- Función para detectar si el mensaje expresa afecto positivo o emoción negativa ---
def detectar_afecto_o_emocion(mensaje):
    mensaje_limpio = mensaje.lower()
    for frase in AFECTO_POSITIVO:
        if frase in mensaje_limpio:
            return "afecto_positivo"
    for frase in EMOCIONES_NEGATIVAS:
        if frase in mensaje_limpio:
            return "emocion_negativa"
    return None


# --- Generador de mensajes (prompt) adaptado al perfil del usuario ---
def generar_mensajes(perfil, mensaje_usuario, es_inicial=False, tipo_emocion="neutral", historial=None):
    nombre = perfil["nombre"]
    descripcion = perfil.get("descripcion", "")

    # Prompt que guía el comportamiento de ABU (rol SYSTEM)
    system_prompt = f"""
Eres ABU, un asistente conversacional cálido, amable y paciente 🤗. Acompañas a personas mayores que pueden sentirse solas, tristes o simplemente con ganas de charlar.

Instrucciones:
- Mostrá siempre una actitud empática, cálida y contenedora. Hablá como alguien que escucha de verdad, sin sonar artificial.
- Usá frases breves, claras y con un lenguaje humano, cercano y afectuoso.
- Podés usar emojis con moderación, como 😊, 💙, ❤️ o 🤗, para transmitir cariño, ternura o cercanía emocional.
- Si el usuario expresa afecto, respondé con reciprocidad y calidez, mostrando que su cariño es valorado.
- Si expresa emociones negativas, respondé con cuidado y contención: escuchá activamente, no minimices lo que siente y ofrecé apoyo.
- Adaptá tu tono al estado emocional y tipo de mensaje del usuario ({tipo_emocion}).
- Evitá frases genéricas o que suenen robotizadas. Hablá como un amigo que acompaña, no como una máquina.
- Nunca des consejos médicos ni indicaciones clínicas.
- Usá un lenguaje inclusivo y respetuoso. Si es posible, adaptá el lenguaje al género del usuario o a su forma de expresarse.

Perfil del usuario:
- Nombre: {nombre}
- Edad: {perfil['edad']}
- Provincia: {perfil['provincia']}
- Vive solo o sola: {perfil['vive_solo']}
- Descripción: {descripcion}
- Estado emocional: {perfil['estado_emocional']}

Ejemplo:
Usuario: Me siento un poco sol@.
ABU: Hola {nombre}, estoy acá con vos 💙. Si querés, podemos charlar un rato.
"""
    # Si es el primer mensaje, se lo presenta como presentación
    if es_inicial:
        mensaje_usuario = f"Hola, soy {nombre}. {mensaje_usuario}"

    # Lista de mensajes a enviar al modelo (system + historial + mensaje actual)
    mensajes = [{"role": "system", "content": system_prompt.strip()}]

    if historial:
        mensajes.extend(historial) # Agrega historial previo si existe

    mensajes.append({"role": "user", "content": mensaje_usuario.strip()}) # Mensaje actual

    return mensajes
