
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
               FROM eventos ORDER BY id"""
        ).fetchall()
        return [dict(linha) for linha in linhas]
    finally:
        conexao.close()


def buscar_evento(evento_id: int):
    conexao = conectar()
    try:
        linha = conexao.execute(
            """SELECT id, nome, capacidade, ingressos_vendidos
               FROM eventos WHERE id = ?""",
            (evento_id,),
        ).fetchone()
        return dict(linha) if linha is not None else None
    finally:
        conexao.close()


def criar_evento(nome: str, capacidade: int):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            """INSERT INTO eventos (nome, capacidade, ingressos_vendidos)
               VALUES (?, ?, 0)""",
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
            """UPDATE eventos
               SET ingressos_vendidos = ingressos_vendidos + ?
               WHERE id = ?
               AND ingressos_vendidos + ? <= capacidade""",
            (quantidade, evento_id, quantidade),
        )

        if cursor.rowcount == 0:
            return None

        conexao.commit()

        linha = conexao.execute(
            """SELECT id, nome, capacidade, ingressos_vendidos
               FROM eventos WHERE id = ?""",
            (evento_id,),
        ).fetchone()

        return dict(linha) if linha is not None else None
    finally:
        conexao.close()


def consultar_disponibilidade(evento_id: int):
    evento = buscar_evento(evento_id)
    if evento is None:
        return None

    return {
        "evento_id": evento["id"],
        "nome": evento["nome"],
        "capacidade": evento["capacidade"],
        "ingressos_vendidos": evento["ingressos_vendidos"],
        "vagas_disponiveis": evento["capacidade"] - evento["ingressos_vendidos"],
    }


def listar_mais_vendidos(limite: int = 3):
    conexao = conectar()
    try:
        linhas = conexao.execute(
            """SELECT id, nome, capacidade, ingressos_vendidos
               FROM eventos
               ORDER BY ingressos_vendidos DESC, id ASC
               LIMIT ?""",
            (limite,),
        ).fetchall()
        return [dict(linha) for linha in linhas]
    finally:
        conexao.close()


def cancelar_ingressos(evento_id: int, quantidade: int):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            """UPDATE eventos
               SET ingressos_vendidos = ingressos_vendidos - ?
               WHERE id = ?
               AND ingressos_vendidos >= ?""",
            (quantidade, evento_id, quantidade),
        )

        if cursor.rowcount == 0:
            return None

        conexao.commit()

        linha = conexao.execute(
            """SELECT id, nome, capacidade, ingressos_vendidos
               FROM eventos WHERE id = ?""",
            (evento_id,),
        ).fetchone()

        return dict(linha) if linha is not None else None
    finally:
        conexao.close()


def atualizar_evento(evento_id: int, nome: str, capacidade: int):
    conexao = conectar()
    try:
        evento = conexao.execute(
            """SELECT id, ingressos_vendidos
               FROM eventos WHERE id = ?""",
            (evento_id,),
        ).fetchone()

        if evento is None:
            return None

        if capacidade < evento["ingressos_vendidos"]:
            return False

        conexao.execute(
            """UPDATE eventos
               SET nome = ?, capacidade = ?
               WHERE id = ?""",
            (nome, capacidade, evento_id),
        )
        conexao.commit()

        linha = conexao.execute(
            """SELECT id, nome, capacidade, ingressos_vendidos
               FROM eventos WHERE id = ?""",
            (evento_id,),
        ).fetchone()

        return dict(linha) if linha is not None else None
    finally:
        conexao.close()


def relatorio_ocupacao():
    conexao = conectar()
    try:
        linha = conexao.execute(
            """SELECT
                   COUNT(*) AS total_eventos,
                   COALESCE(SUM(capacidade), 0) AS capacidade_total,
                   COALESCE(SUM(ingressos_vendidos), 0) AS ingressos_vendidos,
                   COALESCE(SUM(capacidade - ingressos_vendidos), 0) AS vagas_disponiveis
               FROM eventos"""
        ).fetchone()
        return dict(linha)
    finally:
        conexao.close()


def excluir_evento(evento_id: int):
    conexao = conectar()
    try:
        evento = conexao.execute(
            """SELECT id, ingressos_vendidos
               FROM eventos WHERE id = ?""",
            (evento_id,),
        ).fetchone()

        if evento is None:
            return None

        if evento["ingressos_vendidos"] > 0:
            return False

        conexao.execute(
            "DELETE FROM eventos WHERE id = ?",
            (evento_id,),
        )
        conexao.commit()
        return True
    finally:
        conexao.close()
