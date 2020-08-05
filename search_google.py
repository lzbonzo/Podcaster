# -*- coding: utf-8 -*-

import requests

print(requests.get('https://podcasts.google.com/?q=сережа').text)