"""Dados recebidos nas requisições HTTP."""
from pydantic import BaseModel, Field

class EventoEntrada(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    capacidade: int = Field(gt=0)

class PedidoIngressos(BaseModel):
    quantidade: int = Field(gt=0)


