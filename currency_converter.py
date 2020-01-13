import argparse as ap


def add_parameters_needed(args_parser: ap.ArgumentParser):
	"""
	Function for adding all parameters that should be parsed on input of the program
	:param args_parser: object of ArgumentParses class for which the arguments are defined
	:return: Argument parser object with added definitions of input parameters format
	"""
	args_parser.add_argument("--amount", required=True, help="Amount of currency to convert")
	args_parser.add_argument("--input_currency", required=True, help="Currency of the amount on input")
	args_parser.add_argument("--output_currency", required=True, help="Currency of desired output")
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


	print("End of script\n")



