from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import (
    crear_tablas,
    registrar_agente,
    despertar_agente,
    enviar_mensaje,
    leer_mensajes,
    listar_agentes,
)

crear_tablas()

class AgenteRequest(BaseModel):
    nombre: str
    rol: str
    energia: int


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str


app = FastAPI(
    title="Sistema de Agentes",
    description="API para gestionar agentes y mensajes",
)

@app.get("/")
def inicio():
    return {"status": "online", "mensaje": "Bienvenido al sistema de agentes"}


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return agente


@app.get("/agentes/")
def obtener_todos_los_agentes():
    return listar_agentes()

@app.post("/agentes/")
def crear_agente(agente: AgenteRequest):
    resultado = registrar_agente(agente.nombre, agente.rol, agente.energia)
    return {"mensaje": resultado}


@app.post("/mensajes/")
def crear_mensaje(mensaje: MensajeRequest):
    resultado = enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}")
def obtener_mensajes(nombre: str):
    return leer_mensajes(nombre)
