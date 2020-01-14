# Kiwi_currency_converter
 Python app for converting currencies
## About
Program contains CLI and API application for converting currencies.

## Requirements
- Libraries
    - Flask
    
##Input
- amount - amount which we want to convert - float
- input_currency - input currency - 3 letters name or currency symbol
- output_currency - requested/output currency - 3 letters name or currency symbol
    - If missing all available currencies are considered as output_currencies
## Output
JSON file in following format.
```Python
{
    "input": { 
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <3 letter currency code>: <float>
    }
}
```

## External resources
Resource for currencies symbols is Common-Currency.json from https://gist.github.com/Fluidbyte/2973986#file-common-currency-json

Supported currencies are those listed on this site: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html

Used API: GET https://api.ratesapi.io/api/latest HTTP/2