import argparse as ap
import requests
import json
from currency_symbols import get_currency_name


def add_parameters_needed(args_parser: ap.ArgumentParser):
	"""
	Function for adding all parameters that should be parsed on input of the program
	:param args_parser: object of ArgumentParses class for which the arguments are defined
	:return: Argument parser object with added definitions of input parameters format
	"""
	args_parser.add_argument("--amount", required=True, help="Amount of currency to convert")
	args_parser.add_argument("--input_currency", required=True, help="Currency of the amount on input")
	args_parser.add_argument("--output_currency", required=False, help="Currency of desired output")
	return args_parser


class CurrencyConverter:
	def __init__(self, amount_to_convert: float = 0, input_currency: str = None, output_currency: str = None):
		self.amount = amount_to_convert
		self.iCurrency = input_currency
		self.exchangeRates = None
		self.oCurrency = output_currency
		self.resultJSON = None

	def verify_input_currency_name(self):
		self.iCurrency = get_currency_name(self.iCurrency)

	def get_exchange_rates(self):
		self.verify_input_currency_name()
		# Get rates from exchangeratesapi.io
		currency_get = requests.get(f"https://api.exchangeratesapi.io/latest?base={self.iCurrency}")
		if currency_get.status_code == 440:
			# Failed connection
			raise ConnectionError("Unable to retrieve exchange rates from server.")
		elif currency_get.status_code == 400:
			# Usually base currency not supported
			raise ValueError(currency_get.text)
		elif currency_get.status_code != 200:
			raise BaseException(f"Unexpected error during obtaining exchange rates\nCode: {currency_get.status_code} - {currency_get.text}")
		self.exchangeRates = json.loads(currency_get.text)["rates"]
	
	def verify_output_currency_name(self):
		if self.oCurrency is not None:
			self.oCurrency = get_currency_name(self.oCurrency)
			# Check if program have exchange rate for output currency
			if self.oCurrency not in self.exchangeRates.keys():
				raise ValueError(f"Unsupported output currency: {self.oCurrency}")

	def set_result_JSON_string(self):
		try:
			self.verify_output_currency_name()
		except ValueError as e:
			print(e)
			return None
		except BaseException as e:
			print(f"Unexpected error during finding currency name:\n{e}")
			return None

		res_json_dict = {
			"input": {
				"amount": str(self.amount),
				"currency": self.iCurrency
			},
			"output": {
				#  <3 letter currency code>: <float>
			}
		}
		# Fill resJsonDict with one or multiple exchange rates
		if self.oCurrency is None:
			for oCur in self.exchangeRates.keys():
				res_json_dict["output"][oCur] = "%.2f" % (self.amount * float(self.exchangeRates[oCur]))
		else:
			res_json_dict["output"][self.oCurrency] = "%.2f" % (self.amount * float(self.exchangeRates[self.oCurrency]))
		self.resultJSON = json.dumps(res_json_dict, indent=4)


if __name__ == "__main__":
	argsParser = ap.ArgumentParser()
	try:
		argsParser = add_parameters_needed(argsParser)
	except ap.ArgumentError as e:
		print(f"Problem in 'args_parser.add_parameters_needed' function\n{e}")
		exit(2)

	# Get dictionary of parameters and values
	args = vars(argsParser.parse_args())

	# Declare amount for future use (syntax checking)
	amount = 0
	try:
		amount = float(args["amount"])
	except ValueError as valE:
		print("Argument --amount should be numeric (use . as decimal sign)")
		exit(2)
	iCurrency = args["input_currency"]
	oCurrency = args["output_currency"]
	
	# initialize converter class instance
	converter = CurrencyConverter(amount, iCurrency, oCurrency)
	try:
		converter.get_exchange_rates()
	except ValueError as valE:
		print(valE)
		exit(2)
	except ConnectionError as ce:
		print("Problem with connection to database")
		print(ce)
		exit(-1)
	except BaseException as e:
		print(e)
		exit(-1)

	try:
		converter.set_result_JSON_string()
	except ValueError as valE:
		print(valE)
		exit(2)
	except BaseException as e:
		print(e)
		exit(-1)

	resJsonString = converter.resultJSON
	if resJsonString:
		print(resJsonString)
	else:
		exit(2)
