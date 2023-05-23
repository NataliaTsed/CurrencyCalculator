import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyCalculator:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Введите различные валюты: {base}.')
        if base == quote:
            raise APIException(f'Введите различные валюты: {quote}.')
        # quote_ticker, base_ticker = keys[quote], keys[base]
        if float(amount) <= 0:
            raise APIException('Введите сумму больше нуля.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            amount = float(amount)

        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base
