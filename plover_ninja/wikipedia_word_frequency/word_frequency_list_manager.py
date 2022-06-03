#!/usr/bin/env python3

import pathlib

CURR_DIR = pathlib.Path(__file__).parent.absolute()
WORD_FREQUENCY_LIST = pathlib.PurePath(CURR_DIR, 'enwiki-20210820-words-frequency.txt')

def get_word_frequency_list_as_map():
    word_frequency_map = {}
    with open(WORD_FREQUENCY_LIST, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split()
            word_frequency_map[tokens[0]] = tokens[1]
    return word_frequency_map
