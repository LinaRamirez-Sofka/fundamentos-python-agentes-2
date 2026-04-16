from fastapi import FastAPI, HTTPException, Path
from db import (
    crear_tablas,
    registrar_agente,
    despertar_agente,
    enviar_mensaje,
    leer_mensajes,
    listar_agentes,
    registrar_mision,
    obtener_mision,
    listar_misiones_agente,
    actualizar_estado_mision,
    actualizar_energia_agente,
)
from agente import AgenteAdmin, PseudoAgente
from dto import AgenteRequest, AgenteResponse, MensajeRequest, MisionRequest

crear_tablas()

app = FastAPI(
    title="Sistema de Agentes",
    description="API para gestionar agentes y mensajes",
)

@app.get("/")
def inicio():
    return {"status": "online", "mensaje": "Bienvenido al sistema de agentes"}


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    agente_entity = despertar_agente(nombre)
    if agente_entity is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    agente: PseudoAgente
    if agente_entity["rol"] == "admin":
        agente = AgenteAdmin(agente_entity["nombre"],  agente_entity["energia"])
    else:
        agente = PseudoAgente(agente_entity["nombre"],  agente_entity["energia"])
    print(f"El agente despertado es del tipo Admin: {isinstance(agente, AgenteAdmin)}")
    return AgenteResponse(name=agente.name, tokens=agente.tokens)


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

@app.post("/misiones/")
def crear_mision(mision: MisionRequest):
    resultado = registrar_mision(mision.titulo, mision.descripcion, mision.agente_asignado,
                                  mision.tiempo_estimado, mision.energia_requerida)
    if resultado is None:
        raise HTTPException(status_code=404, detail=f"Agente '{mision.agente_asignado}' no encontrado")
    return {"mensaje": resultado}


@app.get("/misiones/{id}")
def obtener_mision_por_id(mision_id: int):
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Mision '{mision_id}' no encontrada")
    return mision


@app.get("/agente/{nombre}/misiones")
def obtener_misiones_de_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return listar_misiones_agente(nombre)


@app.post("/misiones/{id}/completar")
def completar_mision(mision_id: int = Path(..., alias="id")):
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Mision '{mision_id}' no encontrada")

    nombre_agente = mision["agente_asignado"]
    if not nombre_agente:
        raise HTTPException(status_code=400, detail="La mision no tiene agente asignado")

    agente_entity = despertar_agente(nombre_agente)
    if agente_entity is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre_agente}' no encontrado")

    agente: PseudoAgente
    if agente_entity["rol"] == "admin":
        agente = AgenteAdmin(agente_entity["nombre"], agente_entity["energia"])
    else:
        agente = PseudoAgente(agente_entity["nombre"], agente_entity["energia"])

    energia_requerida = mision["energia_requerida"]
    agente.consume_energy(energia_requerida)

    actualizar_energia_agente(agente.name, agente.tokens)
    actualizar_estado_mision(mision_id, "completada")

    return {
        "mensaje": f"Mision '{mision_id}' completada por '{agente.name}'",
        "energia_actual": agente.tokens,
        "tipo_agente": type(agente).__name__,
    }


@app.get("/briefing/{nombre}")
def briefing_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")

    return {
        "agente": agente,
        "briefing": "Briefing generado. La inteligencia externa sera integrada en la siguiente iteracion.",
    }

