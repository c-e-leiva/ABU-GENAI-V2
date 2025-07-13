# perfiles_precargados.py
# Módulo que contiene perfiles precargados para facilitar pruebas o permitir un inicio rápido del asistente.

# Función principal para obtener un perfil completo según el nombre ingresado

def obtener_perfil(nombre):
    # Diccionario con perfiles simulados para usuarios adultos mayores
    perfiles = {
        "rosa": {
            "nombre": "Rosa",
            "edad": 72,
            "provincia": "Santa Fe",
            "descripcion": "Me gusta tejer, leer novelas y mirar televisión. Hace un año perdí a mi esposo y todavía lo tengo mucho presente. Me gusta hablar de él, recordar buenos momentos y sentir que no estoy sola.",
            "vive_solo": "Sí",
            "estado_emocional": "Pensante",
            "dificultades": {
                "memoria": True,
                "vision": False,
                "audicion": True,
                "movilidad": False,
                "comprension": False
            },
            "preferencias": {
                "noticias": True,
                "clima": True,
                "recordatorios": True
            },
            "contacto_emergencia": {
                "nombre": "Claudia",
                "numero": "1123456789",
                "relacion": "Hijx"
            },
            "obra_social": {
                "nombre": "PAMI",
                "telefono": "0800-222-7264"
            },
            "recordatorios": [
                {"descripcion": "Tomar la medicación", "fecha": "12/07/2025", "hora": "08:00"},
                {"descripcion": "Llamar a Claudia", "fecha": "13/07/2025", "hora": "18:30"}
            ]
        },

        "juan": {
            "nombre": "Juan",
            "edad": 74,
            "provincia": "Córdoba",
            "descripcion": "Soy fanático de Boca Juniors desde que tengo memoria. Me encanta el tango, tomar mate con mis amigos y ver partidos con mi nieto. Siempre tengo una anécdota para contar y me gusta mantenerme informado.",
            "vive_solo": "No",
            "estado_emocional": "Feliz",
            "dificultades": {
                "memoria": False,
                "vision": False,
                "audicion": False,
                "movilidad": True,
                "comprension": False
            },
            "preferencias": {
                "noticias": True,
                "clima": True,
                "recordatorios": True
            },
            "contacto_emergencia": {
                "nombre": "Nico",
                "numero": "1145678901",
                "relacion": "Amigx"
            },
            "obra_social": {
                "nombre": "PAMI",
                "telefono": "0800-222-7264"
            },
            "recordatorios": [
                {"descripcion": "Ver el partido de Boca", "fecha": "14/07/2025", "hora": "21:00"},
                {"descripcion": "Cita médica", "fecha": "15/07/2025", "hora": "10:00"}
            ]
        },

        "pedro": {
            "nombre": "Pedro",
            "edad": 68,
            "provincia": "Buenos Aires",
            "descripcion": "Soy Hincha fanático de River, me encanta el asado del domingo y seguir a Messi. Me gusta la carpintería y salir a caminar al parque. A veces me siento un poco bajoneado, pero intento mantenerme activo.",
            "vive_solo": "No",
            "estado_emocional": "Triste",
            "dificultades": {
                "memoria": False,
                "vision": True,
                "audicion": False,
                "movilidad": False,
                "comprension": False
            },
            "preferencias": {
                "noticias": True,
                "clima": True,
                "recordatorios": True
            },
            "contacto_emergencia": {
                "nombre": "Elena",
                "numero": "1134567890",
                "relacion": "Familiar"
            },
            "obra_social": {
                "nombre": "IOMA",
                "telefono": "0810-999-4662"
            },
            "recordatorios": [
                {"descripcion": "Taller de carpintería", "fecha": "12/07/2025", "hora": "15:00"},
                {"descripcion": "Paseo por el parque", "fecha": "13/07/2025", "hora": "17:00"}
            ]
        }
    }

    # Retorna el perfil que coincida con el nombre (ignorando mayúsculas/minúsculas)
    return perfiles.get(nombre.lower())
