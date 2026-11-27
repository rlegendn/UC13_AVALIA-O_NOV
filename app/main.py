
"""API de eventos — projeto para manutenção."""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from . import repositorio
from .schemas import EventoEntrada, PedidoIngressos

app = FastAPI(title="API de Eventos — UC-13", version="0.3")


@app.get("/")
def pagina_inicial():
    return {
        "mensagem": "API de Eventos funcionando!",
        "status": "Online",
    }


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
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )
    return evento


@app.post("/api/eventos", status_code=status.HTTP_201_CREATED)
def cadastrar(dados: EventoEntrada):
    if not dados.nome.strip() or dados.capacidade <= 0:
        raise HTTPException(
            status_code=422,
            detail="Nome e capacidade devem ser válidos"
        )

    evento_id = repositorio.criar_evento(
        dados.nome,
        dados.capacidade
    )
    return {
        "id": evento_id,
        "nome": dados.nome,
        "capacidade": dados.capacidade,
        "ingressos_vendidos": 0,
    }


@app.post("/api/eventos/{evento_id}/ingressos",
          status_code=status.HTTP_201_CREATED)
def comprar_ingressos(evento_id: int, pedido: PedidoIngressos):
    evento = repositorio.buscar_evento(evento_id)

    if evento is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    if pedido.quantidade <= 0:
        raise HTTPException(
            status_code=422,
            detail="A quantidade deve ser positiva"
        )

    atualizado = repositorio.registrar_ingressos(
        evento_id,
        pedido.quantidade
    )

    if atualizado is None:
        raise HTTPException(
            status_code=409,
            detail="Vagas insuficientes"
        )

    return atualizado


@app.get("/api/eventos/{evento_id}/disponibilidade")
def disponibilidade(evento_id: int):
    resultado = repositorio.consultar_disponibilidade(evento_id)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    return resultado


@app.get("/api/relatorios/mais-vendidos")
def mais_vendidos():
    return repositorio.listar_mais_vendidos(3)


@app.post("/api/eventos/{evento_id}/cancelamentos")
def cancelar(evento_id: int, pedido: PedidoIngressos):
    evento = repositorio.buscar_evento(evento_id)

    if evento is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    if pedido.quantidade <= 0:
        raise HTTPException(
            status_code=422,
            detail="A quantidade deve ser positiva"
        )

    atualizado = repositorio.cancelar_ingressos(
        evento_id,
        pedido.quantidade
    )

    if atualizado is None:
        raise HTTPException(
            status_code=409,
            detail="Quantidade de cancelamentos superior às vendas"
        )

    return atualizado


@app.put("/api/eventos/{evento_id}")
def atualizar(evento_id: int, dados: EventoEntrada):
    if not dados.nome.strip() or dados.capacidade <= 0:
        raise HTTPException(
            status_code=422,
            detail="Nome e capacidade devem ser válidos"
        )

    resultado = repositorio.atualizar_evento(
        evento_id,
        dados.nome,
        dados.capacidade
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    if resultado is False:
        raise HTTPException(
            status_code=409,
            detail="Capacidade não pode ser menor que ingressos vendidos"
        )

    return resultado


@app.get("/api/relatorios/ocupacao")
def ocupacao():
    return repositorio.relatorio_ocupacao()


@app.delete("/api/eventos/{evento_id}", status_code=204)
def excluir(evento_id: int):
    resultado = repositorio.excluir_evento(evento_id)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    if resultado is False:
        raise HTTPException(
            status_code=409,
            detail="Evento possui ingressos vendidos e não pode ser excluído"
        )

    return Response(status_code=204)
