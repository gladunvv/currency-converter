import json
import flask
import urllib.request
from flask import request, jsonify, abort
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "it-is-secret-key"


def api_amount():
    if "amount" in request.args:
        amount = request.args["amount"]
        amount = float(amount)
        return amount
    else:
        return abort(400, description="Invalid amount")


def api_input_currency():
    if "input_currency" in request.args:
        input_currency = request.args["input_currency"]
        input_currency = input_currency.upper()
        return input_currency
    else:
        return abort(400, description="Invalid input currency")


def api_output_currency():
    if "output_currency" in request.args:
        output_currency = request.args["output_currency"]
        output_currency = output_currency.upper()
        return output_currency
    else:
        return abort(400, description="Invalid output currency")


def currency_code_check(string):
    string = str(string)
    string = string.upper()
    with open("currency_list.json", "r") as f:
        data = json.load(f)
        result = False
        for currency in data.values():
            if string in currency["code"]:
                result = True
        return result


def input_output_converter(input_currency, output_currency):
    for i in input_currency, output_currency:
        i = str(i)
        if not currency_code_check(i):
            with open("currency_list.json", "r") as f:
                data = json.load(f)

                for currency in data.values():
                    if i in currency["symbol_native"]:
                        if i == input_currency:
                            input_currency = currency["code"]
                        elif i == output_currency:
                            output_currency = currency["code"]
    return input_currency, output_currency


def get_data():
    with urllib.request.urlopen(
        f"http://data.fixer.io/api/latest?access_key={API_KEY}&format=1") as response:
        source = response.read()
    return json.loads(source)


def rate_counting(input_currency, output_currency, data, amount):
    try:
        if input_currency and output_currency in data["rates"]:
            a, b = ((data["rates"][input_currency]), (data["rates"][output_currency]))
            converted_amount = b / a * amount
            return float(converted_amount)
    except KeyError:
        abort(500, "Invalid api key")


def final_json(input_currency, output_currency, amount, converted_amount):
    final_data = ({"input": {"amount": amount,
                             "currency": input_currency},
                   "output": {output_currency: round(converted_amount, 2)}})
    return jsonify(final_data)


@app.route("/currency_converte", methods=["GET"])
def convert():
    amount = api_amount()
    input_currency = api_input_currency()
    output_currency = api_output_currency()
    input_currency, output_currency = input_output_converter(input_currency, output_currency)
    data = get_data()
    converted_amount = rate_counting(input_currency, output_currency, data, amount)
    final_data = final_json(input_currency, output_currency, amount, converted_amount)
    return final_data


@app.errorhandler(400)
def bad_request_error(error):
    message = {
        "error": f"{error}",
    }
    return jsonify(message), 400


@app.errorhandler(500)
def internal_error(error):
    message = {
        "error": f"{error}",
    }
    return jsonify(message), 500


@app.errorhandler(404)
def not_found_error(error):
    message = {
        "error": f"{error}",
    }
    return jsonify(message), 404


app.run(debug=True)
