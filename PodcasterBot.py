#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import time
from threading import Thread
import schedule
import config
import flask
from telebot import types
import telebot
import re
import requests


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
        bot.send_message(message.chat.id, text='Где будем искать?', reply_markup=apple_or_yandex)
        request_word = message
    return


# yandex or apple
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global request_word
    try:
        if call.message:
            if request_word:
                if call.data == 'apple':
                    send_url_apple(request_word)
                elif call.data == 'yandex':
                    send_url_yandex(request_word)
                request_word = None
    except Exception as e:
        print(repr(e))


def send_url_yandex(message, search_type='podcasts'):
    find = f'https://music.yandex.ru/search?text={message.text}&type={search_type}'
    search = requests.get(find).text
    urls = re.findall(r"(/album/.*?)\"", search)
    if len(urls) == 0:
        bot.send_message(message.chat.id, 'Похоже в Yandex еще не подвезли подкасты на эту тему')
    else:
        for url in urls:
            url = 'https://music.yandex.ru' + url
            bot.send_message(message.chat.id, url)


def send_url_apple(message, search_type='podcast'):
    kind = ['podcast', 'podcast-episode']
    search_url = f'https://itunes.apple.com/search?term={message.text}&media={search_type}&country=ru&limit=50'
    json_search = json.loads(requests.get(search_url).text)
    # Проверяем на наличие результатов
    if json_search['resultCount'] == 0:
        bot.send_message(message.chat.id, 'Похоже в Apple еще не подвезли подкасты на эту тему')
    else:
        for res in json_search['results']:
            if res['kind'] in kind:
                bot.send_message(message.chat.id, res['collectionViewUrl'])


# Проверка бота
def check():
    bot.send_message(chat_id=303070030, text='Доброе утро. Я всё ещё жив')


def schedule_checker():
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    schedule.every().day.at("10:00").do(check)  # Если бот жив, то он присылает мне сообщение в 10 утра
    Thread(target=schedule_checker).start()
    bot.polling(none_stop=True, interval=0)
