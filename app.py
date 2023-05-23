import telebot
from config import TOKEN, keys
from exceptions import APIException, CurrencyCalculator

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Для начала работы Вам необходимо ввести данные через пробел в следующем формате:' \
           ' \n1) Название валюты, цену которой Вы хотите узнать;  \n2) Название валюты, в которой Вы хотите узнать ' \
           'цену первой валюты; \n3) Количество первой валюты.\n ' \
           'Пример ввода: доллар евро 1 \n\
 Список доступных валют: /values'

    bot.send_message(message.chat.id, "Дорогой пользователь! \nДобро пожаловать в лучший валютный конвертер!")
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_def(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# base, quote, amount = message.text.split(' ')


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверно введены параметры! Необходимо ввести 3 значения!')

        base, quote, amount = values
        total_base = CurrencyCalculator.get_price(base, quote, amount)
#        text = f'Цена {amount} {base} в {quote}: {total_base}'
#        bot.send_message(message.chat.id, text)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
