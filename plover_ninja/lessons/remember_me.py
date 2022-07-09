#!/usr/bin/env python3

from pathlib import Path
from datetime import date

from plover_ninja.storage import get_rarely_used_words, TEMP_DIR


class RememberMe:
    def __init__(self):
        pass

    # TODO: Make this a class method?
    def make_lesson(self):
        # returns a tuple containing:
        # - count of strokes
        # - word frequency
        # - word
        least_used_words_tuples = get_rarely_used_words()

        longest_word_len = 0
        for _, _, word in least_used_words_tuples:
            word_len = len(word)
            if word_len > longest_word_len:
                longest_word_len = word_len
        word_padding = longest_word_len + 5

        longest_word_id_len = 0
        for _, word_id, _ in least_used_words_tuples:
            word_id_len = len(str(word_id))
            if word_id_len > longest_word_id_len:
                longest_word_id_len = word_id_len
        word_id_padding = longest_word_id_len + 5

        word_list = []
        for stroke_count, word_id, word in least_used_words_tuples:
            text = f'{word:{word_padding}} word #{word_id:<{word_id_padding}} stroke count: {stroke_count}'
            word_list.append(text)
        word_list = '\n'.join(word_list)

        today = date.today()
        file_name_today = today.strftime('%Y%m%d')
        report_text_today = today.strftime('%m/%d/%Y')

        with open(f'{Path(TEMP_DIR) / file_name_today}_remember_me.txt', 'w', encoding='utf-8') as f:
            text = f"""Ninja Lesson
{report_text_today}

You've seen these words, but they're still pretty fresh.
Take some time getting to know them a bit better!

{word_list}

🐦🥋
"""
            f.write(text)
