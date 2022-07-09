#!/usr/bin/env python3

from pathlib import Path
from datetime import date

from plover_ninja.storage import get_most_common_words_that_have_not_been_used_yet, TEMP_DIR


class MakeANewFriend:
    def __init__(self):
        pass

    # TODO: Make this a class method?
    def make_lesson(self, mini_lesson = False):
        frequency_word_tuples = get_most_common_words_that_have_not_been_used_yet()
        longest_word_len = 0
        for _, word in frequency_word_tuples:
            word_len = len(word)
            if word_len > longest_word_len:
                longest_word_len = word_len
        padding = longest_word_len + 5

        word_list = []
        detailed_word_list = []
        for frequency, word in frequency_word_tuples:
            text = f'{word:{padding}} word #{frequency}'
            detailed_word_list.append(text)
            word_list.append(word)
        word_list = '\n'.join(word_list)
        detailed_word_list = '\n'.join(detailed_word_list)

        today = date.today()
        file_name_today = today.strftime('%Y%m%d')
        report_text_today = today.strftime('%m/%d/%Y')

        with open(f'{Path(TEMP_DIR) / file_name_today}_make_a_new_friend.txt', 'w', encoding='utf-8') as f:
            text = f"""Ninja Lesson
{report_text_today}

Make some new friends today! Here are the most common words
that haven't appeared in your writing yet. Give them a try!

{detailed_word_list}

🐦🥋
"""
            f.write(text)

        if mini_lesson:
            return f"""New Words!
----------
{word_list}
"""
        return text
