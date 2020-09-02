# -*- coding: utf-8 -*-

import requests
import json
import telebot
import config

bot = telebot.TeleBot(config.token)


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
