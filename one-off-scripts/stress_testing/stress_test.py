#!/usr/bin/env python3

import logging
import os
import pathlib
import requests
import sqlite3
from random import random
from time import time

from plover_ninja import storage

logger = logging.getLogger(__name__)

# War and Peace
# 432,148 strokes
# Equivalent to a pro stenographer writing
# for 3 days at 8 hours a day and 250 complete words* per minutes
# * = we're treating each word as if it was just a single stroke
war_and_peace_url = 'https://www.gutenberg.org/files/2600/2600-0.txt'

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
DB_FILE = SCRIPT_DIR / "test.db"

# monkey patch storage module's path for ninja.db
storage.DB_FILE = DB_FILE

res = requests.get(war_and_peace_url)
text = res.text
book_words = text.split()

# filter out words that are not in the Words table

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

def write_book():
    """ Simulate writing a book """
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
            t = (word,)
            cursor.execute("""UPDATE Words
                              SET average_stroke_duration_dirty_flag = 1
                              WHERE word = ?
                           """, t)
            words_submitted += 1
            if words_submitted % 1000 == 0:
                logger.info(f'Submitted {words_submitted}..')
        connection.commit()

        batch += 1

def invalidate_average_for_words(num_words=100):
    for word in book_words[:100]:
        t = (word,)
        cursor.execute("""UPDATE Words
                            SET average_stroke_duration_dirty_flag = 1
                            WHERE word = ?
                        """, t)
    connection.commit()


def exercise_queries():
    """ Run Steno Ninja queries that we're interested in testing """
    t1 = time()
    storage.get_most_common_words_that_have_not_been_used_yet()
    t2 = time()

    print(f'get_most_common_words_that_have_not_been_used_yet: {t2-t1}')

    storage.update_average_stroke_duration()
    t1 = time()
    storage.get_slowest_stroked_words()
    t2 = time()

    print(f'get_slowest_stroked_words(num_words: {t2-t1}')

for i in range(100):
    print(f'Trial {i+1}')
    write_book()
    invalidate_average_for_words()
    exercise_queries()
    print('\n----------------------------------------------------------')
