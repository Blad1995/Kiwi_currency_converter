import argparse as ap
import requests
import json
from currency_symbols import get_currency_name
import pprint       # for testing purposes

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
	try:
		iCurrency = get_currency_name(iCurrency)
	except ValueError as valE:
		print(valE)
		exit(2)
	except BaseException as e:
		print(e)
		exit(-1)

	oCurrency = args["output_currency"]

	# Get rates from exchangeratesapi.io
	curGet = requests.get(f"https://api.exchangeratesapi.io/latest?base={iCurrency}")
	if curGet.status_code == 440:
		print("Unable to retrieve exchange rates from server.")
		exit(2)
	elif curGet.status_code == 400:
		print(curGet.text)
		exit(2)
	elif curGet.status_code != 200:
		print("Unexpected error during obtaining exchange rates")
		print(f"Code: {curGet.status_code} - {curGet.text}")

	currencyRates = json.loads(curGet.text)["rates"]

	if oCurrency is not None:
		try:
			oCurrency = get_currency_name(oCurrency)
		except ValueError as e:
			print(e)
			exit(2)
		except BaseException as e:
			print(f"Unexpected error during finding currency name:\n{e}")
			exit(-1)

		if oCurrency not in currencyRates.keys():
			print(f"Unsupported output currency: {oCurrency}")
			exit(2)

	resJsonDict = {
		"input": {
			"amount": amount.__str__(),
			"currency": iCurrency
		},
		"output": {
			#  <3 letter currency code>: <float>
		}
	}

	# Fill resJsonDict with one or multiple exchange rates
	if oCurrency is None:
		for oCur in currencyRates.keys():
			resJsonDict["output"][oCur] = "%.2f" % (amount * float(currencyRates[oCur]))
	else:
		resJsonDict["output"][oCurrency] = "%.2f" % (amount * float(currencyRates[oCurrency]))

	resJsonString = json.dumps(resJsonDict, indent=4)

	print(resJsonString)
