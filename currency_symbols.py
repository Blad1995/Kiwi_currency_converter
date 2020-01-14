import json
import codecs


def read_currency_JSON(json_filename: str):
	"""
	Reads JSON file with currency info.
	:param json_filename: name of the JSON file
	:return: dictionary containing currency info
	"""
	if json_filename:
		with codecs.open(json_filename, "r", encoding="utf-8") as f:
			read_dict = json.load(f)
	else:
		read_dict = None
	return read_dict


def get_symbols_currency_dict(currency_info: dict):
	"""
	Inverts the dictionary structure from {currency_name:{symbol:---,.....}} to {symbol:currency_name}
	:param currency_info: Dictionary with info about currencies
	:return: Dictionary with structure {symbol:currency_name}
	"""
	res_dict = {}
	for key, info in currency_info.items():
		cur_symbol = info["symbol"]
		res_dict[cur_symbol] = key

	return res_dict


def get_currency_name(input_text: str):
	"""
	Search currency info for the name of the currency.
	Either input_text contains valid currency name or valid currency symbol. Otherwise raise exception.
	:type input_text: str
	:param input_text: text which is tested to be name or symbol of currency
	:return: official 3 letters name of currency
	"""
	currency_info = read_currency_JSON("Common-Currency.json")
	symbol_dict = get_symbols_currency_dict(currency_info)
	# Search for corresponding name of currency
	if input_text in currency_info.keys():
		return input_text
	if input_text in symbol_dict.keys():
		return symbol_dict[input_text]
	else:
		raise ValueError(f"'{input_text}' is not a valid currency")
