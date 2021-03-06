# -*- coding: utf-8 -*-

import requests
import telebot
import config
import re


bot = telebot.TeleBot(config.token)


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
