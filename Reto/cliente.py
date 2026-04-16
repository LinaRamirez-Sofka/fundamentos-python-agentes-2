# -----------------------------------------------------------#
# Semana 5 - Sesion 2 (Capitulos 6-7): Cliente HTTP
# -----------------------------------------------------------#
# Este script es el CLIENTE que se comunica con el servidor
# FastAPI (S5_sesion_2.py). Debes ejecutarlo en una TERMINAL
# SEPARADA mientras el servidor esta corriendo.
#
# Requisitos:
# 1. Instala requests (solo la primera vez):
#       pip install requests
# 2. En otra terminal, el servidor debe estar corriendo:
#       cd S5
#       uvicorn S5_sesion_2:app --reload
# 3. Ejecuta este script:
#       python S5_cliente.py
# -----------------------------------------------------------#

import requests

BASE_URL = "http://localhost:8000"

def consultar_agente_http(nombre: str) -> dict | None:
    """Consulta un agente a traves del API usando requests.get()."""
    respuesta = requests.get(f"{BASE_URL}/agente/{nombre}")
    if respuesta.status_code == 200:
        return respuesta.json()
    elif respuesta.status_code == 404:
        print(f"[Cliente] Agente '{nombre}' no encontrado (404)")
        return None
    else:
        print(f"[Cliente] Error inesperado: {respuesta.status_code}")
        return None


def enviar_mensaje_http(remitente: str, destinatario: str, contenido: str) -> dict:
    """Envia un mensaje a traves del API usando requests.post()."""
    datos = {"remitente": remitente, "destinatario": destinatario, "contenido": contenido}
    respuesta = requests.post(f"{BASE_URL}/mensajes/", json=datos)
    return respuesta.json()




if __name__ == "__main__":
    # 1. Verificar que el servidor esta activo
    respuesta = requests.get(f"{BASE_URL}/")
    print(f"Servidor: {respuesta.json()}")

    # 2. Registrar un agente via POST
    nuevo_agente = {"nombre": "Orion", "rol": "estratega", "energia": 130}
    respuesta = requests.post(f"{BASE_URL}/agentes/", json=nuevo_agente)
    print(f"Registrar agente: {respuesta.json()}")

    # 3. Consultar el agente via GET
    agente = consultar_agente_http("Orion")
    print(f"Agente consultado: {agente}")

    # 4. Enviar un mensaje via POST
    resultado = enviar_mensaje_http("Orion", "Atlas", "Solicito reporte de la mision.")
    print(f"Mensaje enviado: {resultado}")

    # 5. Consultar bandeja de Atlas via GET
    respuesta = requests.get(f"{BASE_URL}/mensajes/Atlas")
    mensajes = respuesta.json()
    print(f"\n--- Bandeja de Atlas ({len(mensajes)} mensajes) ---")
    for msg in mensajes:
        print(f"  [{msg['timestamp']}] {msg['remitente']} -> {msg['contenido']}")

