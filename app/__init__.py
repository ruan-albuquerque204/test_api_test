from flask import Flask, jsonify, request

from . import configs

app = Flask(__name__)


@app.route("/user/<string:fiscal_number>", methods=["GET"])
def get_user(fiscal_number: str):
    if not (user_data := configs.load_users().get(fiscal_number)):
        return jsonify({"code": None, "name": None}), 404

    return jsonify(user_data), 200


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

    return jsonify("Usuário salvo com sucesso"), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/", methods=["GET"])
def main():
    return "Ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
