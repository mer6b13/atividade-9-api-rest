from flask import Flask, request, jsonify
import sqlite3
from typing import Any, TypeGuard

app = Flask(__name__)

BANCO = "tarefas.db"


def conectar_banco():
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT DEFAULT '',
            concluida INTEGER DEFAULT 0
        )
    """)

    conexao.commit()
    conexao.close()


def dados_validos(dados: Any) -> TypeGuard[dict[str, Any]]:
    return isinstance(dados, dict)


def validar_dados(dados: dict[str, Any]) -> str | None:
    titulo = dados.get("titulo")

    if not isinstance(titulo, str) or not titulo.strip():
        return "O título da tarefa é obrigatório."

    descricao = dados.get("descricao", "")

    if not isinstance(descricao, str):
        return "A descrição deve ser um texto."

    concluida = dados.get("concluida", False)

    if not isinstance(concluida, bool):
        return "O campo concluida deve ser verdadeiro ou falso."

    return None


def tarefa_para_json(tarefa: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": tarefa["id"],
        "titulo": tarefa["titulo"],
        "descricao": tarefa["descricao"],
        "concluida": bool(tarefa["concluida"])
    }


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "API de tarefas funcionando!"
    }), 200


@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    conexao = conectar_banco()

    tarefas = conexao.execute(
        "SELECT * FROM tarefas"
    ).fetchall()

    conexao.close()

    resultado = [
        tarefa_para_json(tarefa)
        for tarefa in tarefas
    ]

    return jsonify(resultado), 200


@app.route("/tarefas/<int:id>", methods=["GET"])
def buscar_tarefa(id):
    conexao = conectar_banco()

    tarefa = conexao.execute(
        "SELECT * FROM tarefas WHERE id = ?",
        (id,)
    ).fetchone()

    conexao.close()

    if tarefa is None:
        return jsonify({
            "erro": "Tarefa não encontrada."
        }), 404

    return jsonify(tarefa_para_json(tarefa)), 200


@app.route("/tarefas", methods=["POST"])
def adicionar_tarefa():
    dados = request.get_json(silent=True)

    if not dados_validos(dados):
        return jsonify({
            "erro": "Os dados devem estar em formato JSON."
        }), 400

    erro = validar_dados(dados)

    if erro is not None:
        return jsonify({"erro": erro}), 400

    titulo = dados["titulo"].strip()
    descricao = dados.get("descricao", "").strip()
    concluida = dados.get("concluida", False)

    conexao = conectar_banco()

    try:
        cursor = conexao.execute("""
            INSERT INTO tarefas (titulo, descricao, concluida)
            VALUES (?, ?, ?)
        """, (titulo, descricao, int(concluida)))

        conexao.commit()

        tarefa = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        if tarefa is None:
            return jsonify({
                "erro": "Não foi possível cadastrar a tarefa."
            }), 500

        return jsonify(tarefa_para_json(tarefa)), 201

    finally:
        conexao.close()


@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    dados = request.get_json(silent=True)

    if not dados_validos(dados):
        return jsonify({
            "erro": "Os dados devem estar em formato JSON."
        }), 400

    erro = validar_dados(dados)

    if erro is not None:
        return jsonify({"erro": erro}), 400

    titulo = dados["titulo"].strip()
    descricao = dados.get("descricao", "").strip()
    concluida = dados.get("concluida", False)

    conexao = conectar_banco()

    try:
        tarefa = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (id,)
        ).fetchone()

        if tarefa is None:
            return jsonify({
                "erro": "Tarefa não encontrada."
            }), 404

        conexao.execute("""
            UPDATE tarefas
            SET titulo = ?, descricao = ?, concluida = ?
            WHERE id = ?
        """, (titulo, descricao, int(concluida), id))

        conexao.commit()

        tarefa_atualizada = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (id,)
        ).fetchone()

        return jsonify(tarefa_para_json(tarefa_atualizada)), 200

    finally:
        conexao.close()


@app.route("/tarefas/<int:id>", methods=["DELETE"])
def excluir_tarefa(id):
    conexao = conectar_banco()

    try:
        tarefa = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (id,)
        ).fetchone()

        if tarefa is None:
            return jsonify({
                "erro": "Tarefa não encontrada."
            }), 404

        conexao.execute(
            "DELETE FROM tarefas WHERE id = ?",
            (id,)
        )

        conexao.commit()

        return jsonify({
            "mensagem": "Tarefa excluída com sucesso."
        }), 200

    finally:
        conexao.close()


if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)
