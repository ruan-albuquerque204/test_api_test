import datetime as dt
from decimal import Decimal

from flask import Flask, jsonify, request

from . import configs
from . import utils

app = Flask(__name__)


@app.route("/user/<string:fiscal_number>", methods=["GET"])
def get_user(fiscal_number: str):
    fiscal_number = "".join(tuple(filter(str.isdigit, fiscal_number)))
    if not (user_name := configs.load_users().get(fiscal_number)):
        return jsonify(), 404

    return jsonify({"code": fiscal_number, "name": user_name}), 200


@app.route("/debitos/<string:fiscal_number>", methods=["GET"])
def situação_usuario(fiscal_number: str):
    fiscal_number = "".join(tuple(filter(str.isdigit, fiscal_number)))
    if not (debits := configs.load_debits()) or not (debits.get(fiscal_number)):
        return jsonify(), 404

    json_response = {
        "status": "OK",
        "total": Decimal(),
        "quantidade": 0,
        "inadimplencias": {"titulos": [], "total": Decimal(), "quantidade": 0},
        "adimplencias": {"titulos": [], "total": Decimal(), "quantidade": 0},
    }

    today = dt.datetime.today()
    for d in debits[fiscal_number]:
        value = Decimal(d["value"])
        d["value"] = utils.convert_money(d["value"])

        json_response["total"] += value
        json_response["quantidade"] += 1

        if dt.datetime.strptime(d["vencimento"], "%d/%m/%y") < today:
            json_response["inadimplencias"]["titulos"].append(d)
            json_response["inadimplencias"]["total"] += value
            json_response["inadimplencias"]["quantidade"] += 1
            json_response["status"] = "PENDENTE"
            continue

        json_response["adimplencias"]["titulos"].append(d)
        json_response["adimplencias"]["total"] += value
        json_response["adimplencias"]["quantidade"] += 1

    json_response["total"] = utils.convert_money(json_response["total"])
    json_response["inadimplencias"]["total"] = utils.convert_money(
        json_response["inadimplencias"]["total"]
    )
    json_response["adimplencias"]["total"] = utils.convert_money(
        json_response["adimplencias"]["total"]
    )

    return jsonify(json_response), 200


@app.route("/user", methods=["POST"])
def create_user():
    json: dict = request.get_json()

    code = json.get("code")
    name = json.get("name")

    if not code or not name:
        return jsonify("Não foram passadas as coisas"), 400
    elif not len(code) in (11, 14):
        return jsonify("CPF/CNPJ estão incorretos"), 400

    try:
        configs.append_user(code, name)
    except:
        return jsonify("Não foi possível salvar o usuário"), 500

    return jsonify("Usuário salvo com sucesso"), 201


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/", methods=["GET"])
def main():
    return "Ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
