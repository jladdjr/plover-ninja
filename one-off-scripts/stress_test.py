#!/usr/bin/env python3

import requests

war_and_peace_url = 'https://www.gutenberg.org/files/2600/2600-0.txt'

res = requests.get(war_and_peace_url)
text = res.text
words = text.split()
