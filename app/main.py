"""API de eventos — projeto recebido para manutenção."""
from fastapi import FastAPI, HTTPException, status
from . import repositorio
from .schemas import EventoEntrada, PedidoIngressos

app = FastAPI(title="API de Eventos — UC-13", version="0.2")
# @app.get("/")
# def pagina_inicial():
#     return {
#         "mensagem": "API de Eventos funcionando!",
#         "status": "Online",
#     }

@app.get("/api/saude")
def saude():
     return {"status": "ok", "servico": "eventos"}

@app.get("/api/eventos")
def listar():
    return repositorio.listar_eventos()

@app.get("/api/eventos/{evento_id}")
def consultar(evento_id: int):
    evento = repositorio.buscar_evento(evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return evento

@app.post("/api/eventos", status_code=status.HTTP_201_CREATED)
def cadastrar(dados: EventoEntrada):
    evento_id = repositorio.criar_evento(dados.nome, dados.capacidade)
    return {"id": evento_id, "nome": dados.nome, "capacidade": dados.capacidade,
            "ingressos_vendidos": 0}

@app.post("/api/eventos/{evento_id}/ingressos", status_code=status.HTTP_201_CREATED)
def comprar_ingressos(evento_id: int, pedido: PedidoIngressos):
    evento = repositorio.buscar_evento(evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    atualizado = repositorio.registrar_ingressos(evento_id, pedido.quantidade)
    return atualizado

@app.get("/api/eventos/{evento_id}/disponibilidade")
def disponibilidade(evento_id: int):
    resultado = repositorio.consultar_disponibilidade(evento_id)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return resultado

@app.get("/api/relatorios/mais-vendidos")
def relatorio_mais_vendidos():
    return repositorio.listar_mais_vendidos()

@app.post("/api/eventos/{evento_id}/cancelamentos")
def cancelar_ingressos(evento_id: int, pedido: PedidoIngressos):
    resultado = repositorio.cancelar_ingressos(evento_id, pedido.quantidade)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return resultado
