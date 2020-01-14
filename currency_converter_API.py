from flask import Flask, jsonify, abort
from flask_restful import Api, reqparse
from currency_converter import CurrencyConverter

# Initialize FLASK API
app = Flask(__name__)
api = Api(app)


@app.route("/currency_converter", methods=["GET"])
def get_conversion():
	"""
	Default GET function to use CurrencyConverter via API.
	:return: JSON file and status code of the GET request response
	"""
	# Query parser
	arg_parser = reqparse.RequestParser()
	arg_parser.add_argument("amount", required=True, help="Amount of currency to convert")
	arg_parser.add_argument("input_currency", required=True, help="Currency of the amount on input")
	arg_parser.add_argument("output_currency", required=False, help="Currency of desired output")
	args = arg_parser.parse_args()

	if args["input_currency"] == "" or args["amount"] == "":
		abort(400, description="Invalid arguments amount or input_currency")

	converter = CurrencyConverter(args["amount"], args["input_currency"], args["output_currency"])
	try:
		converter.get_exchange_rates()
	except ValueError as valE:
		abort(400, description=str(valE))
	except ConnectionError as ce:
		error_message = f"Problem with connection to database\n{ce}"
		abort(400, description=error_message)
	except BaseException as e:
		abort(400, description=repr(e))

	try:
		converter.set_result_JSON_string()
	except ValueError as valE:
		return valE
	except BaseException as e:
		return e
	if converter.resultDict is None:
		# If error occurred during converting currencies.
		error_message = f"""Unable to get the result for following arguments:\n
						amount: {converter.amount}, input_currency: {converter.iCurrency}, output_currency: {converter.oCurrency}	
					"""
		abort(400, description=error_message)

	return jsonify(converter.resultDict), 200


if __name__ == "__main__":
	app.run()

