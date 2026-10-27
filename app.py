
from flask import Flask, request, jsonify, render_template
from database import conectar, criar_tabelas
from datetime import date
import sqlite3

app = Flask(__name__)
criar_tabelas()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/lancamentos", methods=["POST"])
def cadastrar_lancamento():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido"}), 400

    descricao = dados.get("descricao")
    tipo = dados.get("tipo")
    valor = dados.get("valor")

    if not isinstance(descricao, str) or not descricao.strip():
        return jsonify({"erro": "Descricao obrigatoria"}), 400

    if tipo not in ("receita", "despesa"):
        return jsonify({"erro": "Tipo invalido"}), 400

    if (type(valor) not in (int, float)
            or not 0 < valor < float("inf")):
        return jsonify({"erro": "Valor invalido"}), 400

    with conectar() as conexao:
        conexao.execute("""
            INSERT INTO lancamentos
            (descricao, tipo, valor, data)
            VALUES (?, ?, ?, ?)
        """, (
            descricao.strip(),
            tipo,
            valor,
            date.today().isoformat()
        ))

    return jsonify({
        "mensagem": "Lancamento cadastrado!"
    }), 201


@app.route("/lancamentos", methods=["GET"])
def listar_lancamentos():
    with conectar() as conexao:
        conexao.row_factory = sqlite3.Row
        registros = conexao.execute(
            "SELECT * FROM lancamentos ORDER BY id DESC"
        ).fetchall()

    return jsonify([dict(item) for item in registros])


@app.route("/resumo", methods=["GET"])
def resumo_financeiro():
    with conectar() as conexao:
        resultado = conexao.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN tipo = 'receita'
                    THEN valor ELSE 0 END), 0),
                COALESCE(SUM(CASE WHEN tipo = 'despesa'
                    THEN valor ELSE 0 END), 0)
            FROM lancamentos
        """).fetchone()

    receitas = round(resultado[0], 2)
    despesas = round(resultado[1], 2)
    lucro_liquido = round(receitas - despesas, 2)

    return jsonify({
        "total_receitas": receitas,
        "total_despesas": despesas,
        "lucro_liquido": lucro_liquido
    })


if __name__ == "__main__":
    app.run(debug=True)
