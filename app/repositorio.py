"""Operações da API sobre o arquivo SQLite do projeto."""
import os
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAMINHO_BANCO = Path(os.environ.get(
    "UC13_DB_PATH", str(RAIZ / "dados" / "eventos.db")
))

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao

def listar_eventos():
    conexao = conectar()
    try:
        linhas = conexao.execute(
            """SELECT id, nome, capacidade, ingressos_vendidos
               FROM eventos
               
               ORDER BY id"""
        ).fetchall()
        return [dict(linha) for linha in linhas]
    finally:
        conexao.close()

def buscar_evento(evento_id: int):
    conexao = conectar()
    try:
        linha = conexao.execute(
            "SELECT id, nome, capacidade, ingressos_vendidos FROM eventos WHERE id = ?",
            (evento_id,),
        ).fetchone()
        return dict(linha) if linha is not None else None
    finally:
        conexao.close()

def criar_evento(nome: str, capacidade: int):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            "INSERT INTO eventos (nome, capacidade, ingressos_vendidos) VALUES (?, ?, 0)",
            (nome, capacidade),
        )
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()

def registrar_ingressos(evento_id: int, quantidade: int):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            """
            UPDATE eventos
            SET ingressos_vendidos = ingressos_vendidos + ?
            WHERE id = ?
            AND ingressos_vendidos + ? <= capacidade
            """,
            (quantidade, evento_id, quantidade),
        )

        if cursor.rowcount == 0:
            return None

        conexao.commit()

        linha = conexao.execute(
            "SELECT id, nome, capacidade, ingressos_vendidos FROM eventos WHERE id = ?",
            (evento_id,),
        ).fetchone()

        return dict(linha) if linha is not None else None

    finally:
        conexao.close()
