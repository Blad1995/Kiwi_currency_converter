import json
import codecs


def read_currency_JSON(json_filename: str):
	if json_filename:
		with codecs.open(json_filename, "r", encoding="utf-8") as f:
			read_dict = json.load(f)
	else:
		read_dict = None
	return read_dict


def get_symbols_currency_dict(currency_info:dict):
	res_dict = {}
	for key, info in currency_info.items():
		cur_symbol = info["symbol"]
		res_dict[cur_symbol] = key

	return res_dict


def get_currency_name(symbol: str):
	currency_info = read_currency_JSON("Common-Currency.json")
	symbol_dict = get_symbols_currency_dict(currency_info)
	# Search for corresponding name of currency
	if symbol in currency_info.keys():
		return symbol
	if symbol in symbol_dict.keys():
		return symbol_dict[symbol]
	else:
		raise ValueError(f"'{symbol}' is not a valid currency")
