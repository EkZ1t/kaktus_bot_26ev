import json 
from os.path import exists

import telebot
from telebot import types

from parsing import main, today

token = '5933664101:AAElPs__NRnlIrpxNUVYD8dc3feq0vArNEM'
bot = telebot.TeleBot(token)

def get_keyboard() -> types.InlineKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup()
    with open(f'news_{today}.json', 'r') as file:
        for number, news in enumerate(json.load(file)):
            inline_keyboard.add(types.InlineKeyboardButton(
                text=news['title'],
                callback_data=str(number)
            ))
    return inline_keyboard


@bot.callback_query_handler(func=lambda callback: True)
def send_news_detail(callback: types.CallbackQuery):
    with open(f'news_{today}.json', 'r') as file:
        news = json.load(file)[int(callback.data)]
        bot.send_message(callback.message.chat.id, f'{news["title"]} \n {news["description"]} \n {news["photo"]}')

@bot.message_handler(commands=['start', 'hi'])
def start_bot(message: types.Message):
    if not exists(f'news_{today}.json'):
        main()
    bot.send_message(message.chat.id, f'привет, {message.from_user.first_name} , новости на сегодня: ', reply_markup=get_keyboard())

    
bot.polling()

# TODO: поправить создание файлa 
# TODO: добавить кнопку 'Quit'