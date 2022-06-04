#!/usr/bin/env python3

import logging
import os
import pathlib
import requests
import sqlite3
from random import random
from time import time

import pdb
pdb.set_trace()

logger = logging.getLogger(__name__)

# War and Peace
# 432,148 strokes
# Equivalent to a pro stenographer writing
# for 3 days at 8 hours a day and 250 complete words* per minutes
# * = we're treating each word as if it was just a single stroke
war_and_peace_url = 'https://www.gutenberg.org/files/2600/2600-0.txt'

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
DB_FILE = SCRIPT_DIR / "test.db"

res = requests.get(war_and_peace_url)
text = res.text
book_words = text.split()

# filter out words that are not in the Words table

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# simulate writing book

timestamp = time()
batch = 0
batch_size = 10000
while True:
    # calculate indices
    lower = batch * batch_size
    if lower > len(book_words):
        logger.info(f'Finished processing batches!')
        break
    upper = min(lower + batch_size, len(book_words))

    logger.info(f'Processing batch #{batch}')
    logger.info(f'Batch indices: [{lower}, {upper}]')

    # submit insert statements
    words_submitted = 0
    for word in book_words[lower:upper]:
        stroke_duration = random() * 4
        t = (timestamp, stroke_duration, word)
        cursor.execute("""INSERT INTO Strokes(word_id, timestamp, stroke_duration)
                        SELECT Words.word_id, ?, ?
                        FROM Words
                        WHERE Words.word = ? LIMIT 1
                    """, t)
        words_submitted += 1
        if words_submitted % 1000 == 0:
            logger.info(f'Submitted {words_submitted}..')
    connection.commit()

    batch += 1
