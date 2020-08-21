#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

import config
import flask
from telebot import types
import telebot
import search_apple
import search_yandex

bot = telebot.TeleBot(config.token)
server = flask.Flask(__name__)
request_word = None


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global request_word
    # список слов, по которым не ищем
    stop_words = ['подкасты', 'подкаст', 'podcasts', 'podcast']
    # клавиатура на зону поиска
    find_area = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Подкасты", callback_data='podcast')
    item2 = types.InlineKeyboardButton("Выпуски", callback_data='episode')
    item3 = types.InlineKeyboardButton("Везде", callback_data='anywhere')
    find_area.add(item1, item2, item3)
    # клавиатура на ресурс поиска
    apple_or_yandex = types.InlineKeyboardMarkup()
    apple_button = types.InlineKeyboardButton("Apple.Подкасты", callback_data='apple')
    yandex_button = types.InlineKeyboardButton("Яндекс.Подкасты", callback_data='yandex')
    apple_or_yandex.add(apple_button, yandex_button)
    # Приветствие
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Ну, привет!\nДавай попробуем найти интересующий тебя подкаст.\n'
                                               'По каким словам будем искать?')
    elif message.text.lower() in stop_words:
        bot.send_message(message.from_user.id, 'Ха-ха... Смешно. Давай попробуем ввести более точное название')
    else:
        request_word = message
        bot.send_message(message.chat.id, text='Где будем искать?', reply_markup=apple_or_yandex)
    return


# yandex or apple
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'apple':
                search_apple.send_url_apple(request_word)
            elif call.data == 'yandex':
                search_yandex.send_url_yandex(request_word)
    except Exception as e:
        print(repr(e))


@bot.add_channel_post_handler
def check():
    if time.strftime('%H:%M') == '15:40':
        bot.send_message(chat_id='@roman_allaberdin', text='Я жив!')




if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
