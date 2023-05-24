import telebot
from config import TOKEN, keys
from exceptions import APIException, CurrencyCalculator

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Для начала работы Вам необходимо ввести данные через пробел в следующем формате: \n' \
        ' \n1) Название валюты, цену которой Вы хотите узнать;  \n2) Название валюты, в которой Вы хотите узнать ' \
           'цену первой валюты; \n3) Количество первой валюты.\n' \
           '\nПример ввода конверсии 100 долларов в евро: доллар евро 100 \n\
 \nСписок доступных валют: /values'

    bot.send_message(message.chat.id, "Дорогой пользователь! \nДобро пожаловать в лучший валютный конвертер! :-)")
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_def(message: telebot.types.Message):
    text = 'Вам доступны следующие валюты:'
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

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {base} в {quote}: {round(float(amount) / float(total_base), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
