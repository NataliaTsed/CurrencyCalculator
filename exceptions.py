import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyCalculator:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Надо ввести различные валюты: {base}.')
        if base == quote:
            raise APIException(f'Надо ввести различные валюты: {quote}.')
        if base.isdigit():
            raise APIException("В названии валют цифр нет! ;-) ")
        if quote.isdigit():
            raise APIException("В названии валют цифр нет! ;-) ")
        # quote_ticker, base_ticker = keys[quote], keys[base]
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Введено некорректное название валюты {base}! Мне такая валюта не известна!')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Введено некорректное название валюты {quote}! Выберите валюту из /values')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount} ! Вводи только цифры!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base
