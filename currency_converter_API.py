from flask import Flask, jsonify, abort
from flask_restful import Api, reqparse
from currency_converter import CurrencyConverter

app = Flask(__name__)
api = Api(app)


@app.route("/currency_converter", methods=["GET"])
def get_conversion():
	arg_parser = reqparse.RequestParser()
	arg_parser.add_argument("amount", required=True, help="Amount of currency to convert")
	arg_parser.add_argument("input_currency", required=True, help="Currency of the amount on input")
	arg_parser.add_argument("output_currency", required=False, help="Currency of desired output")
	args = arg_parser.parse_args()

	converter = CurrencyConverter(args["amount"], args["input_currency"], args["output_currency"])
	try:
		converter.get_exchange_rates()
	except ValueError as valE:
		return valE
	except ConnectionError as ce:
		print("Problem with connection to database")
		print(ce)
		exit(-1)
	except BaseException as e:
		return e

	try:
		converter.set_result_JSON_string()
	except ValueError as valE:
		return valE
	except BaseException as e:
		return e
	if converter.resultDict is None:
		error_message = f"""Unable to get the result for following arguments:\n
						amount: {converter.amount}, input_currency: {converter.iCurrency}, output_currency: {converter.oCurrency}	
					"""
		abort(400, description=error_message)
	return jsonify(converter.resultDict), 200


if __name__ == "__main__":
	app.run()

