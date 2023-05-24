import telebot
from config import TOKEN, keys
from exceptions import APIException, CurrencyCalculator

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Для начала работы введи данные через пробел в следующем формате: \n' \
        ' \n1) Название валюты, цену которую хочешь узнать;  \n2) Название валюты, в которой хочешь узнать ' \
           'цену первой валюты; \n3) Количество первой валюты.\n' \
           '\nПример ввода конверсии 100 долларов в евро: доллар евро 100 \n\
 \nСписок доступных валют: /values'

    bot.send_message(message.chat.id, "Дорогой пользователь!🤗 \n"
                                      "Добро пожаловать в руки Гуру валютных операций! 💱 ")
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEJF4hkbhqTI295Ogk2ZGZQYwbUyFdccwAC2wADmL-ADTKdOUX4uisaLwQ")
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_def(message: telebot.types.Message):
    text = 'Рад предложить следующие виды валют:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# base, quote, amount = message.text.split(' ')


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Ты ввел много данных! Для расчета мне необходимо лишь 3 значения!')

        base, quote, amount = values
        total_base = CurrencyCalculator.get_price(base, quote, amount)
        if float(amount) == 0:
            raise APIException('Введи сумму больше нуля! Иначе я не смогу тебе помочь! :-)')
        if float(amount) <= 0:
            raise APIException('Введи положительное количество! В кредит не меняю! :-)')

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя 😳. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду 😵‍💫\n{e}')
    else:
        text = f'Стоимость {amount} {base} в {quote}: {round(float(amount) / float(total_base), 2)}'
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, 'С тобой приятно иметь дело! 🤝')
        bot.send_message(message.chat.id, 'Буду ждать тебя еще! 👀')
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEJF5xkbiDrkPoQb-KvSF-HokVBpqefiAACyQADmL-ADZ3o05MJ4JudLwQ")


bot.polling(none_stop=True)
