#!/usr/bin/env python3

from pathlib import Path
from datetime import date

from plover_ninja.storage import get_slowest_stroked_words, TEMP_DIR


class NeedForSpeed:
    def __init__(self):
        pass

    # TODO: Make this a class method?
    def make_lesson(self, mini_lesson=False):
        # Returns tuples containing:
        # - word_id
        # - word
        # - practice weight
        # - average duration
        # - weighted duration
        average_stroke_duration_tuples = get_slowest_stroked_words()

        if len(average_stroke_duration_tuples) == 0:
            return 'Cannot recommend any words for speedstudy; \n' + \
                   'no words have been written yet!'

        # TODO: make this a util function
        longest_word_len = 0
        for _, word, _, _, _ in average_stroke_duration_tuples:
            word_len = len(word)
            if word_len > longest_word_len:
                longest_word_len = word_len
        word_padding = longest_word_len + 5

        # TODO: make this a util function
        longest_word_id_len = 0
        for word_id, _, _, _, _ in average_stroke_duration_tuples:
            word_id_len = len(str(word_id))
            if word_id_len > longest_word_id_len:
                longest_word_id_len = word_id_len
        word_id_padding = longest_word_id_len + 5

        word_list = []
        detailed_word_list = []
        for word_id, word, practice_weight, average_duration, weighted_duration in average_stroke_duration_tuples:
            text = f'{word:{word_padding}} word #{word_id:<{word_id_padding}} avg stroke duration: {average_duration:.3f}  weighted duration: {weighted_duration:.3f}'
            detailed_word_list.append(text)
            word_list.append(word)
        detailed_word_list = '\n'.join(detailed_word_list)
        word_list = '\n'.join(word_list)

        today = date.today()
        file_name_today = today.strftime('%Y%m%d')
        report_text_today = today.strftime('%m/%d/%Y')

        with open(f'{Path(TEMP_DIR) / file_name_today}_need_for_speed.txt', 'w', encoding='utf-8') as f:
            text = f"""Ninja Lesson
{report_text_today}

Take these words out for some speed practice in order to boost
your overall efficiency. Here are some tips for speed practice:

- Consider using a metronome (digital, physical, whatever is handy)
- Find a starting tempo where you feel _absolutely comfortable_
  stenoing the words. This may feel incredibly slow to you. That's okay!
- Very slowly, bump up the speed as you start to feel more comfortable
  with the words. Pushing a bit beyond your edge is good. Try to
  avoid straining too much though. Bring the tempo back down as
  needed.
- While you practice, look for 'speed bumps'. A speed bump may be:
  - a mental pause to remember a translation
  - a mental pause while you try to recall a handshape
  - a physical delay while you try to make the shape of a chord
  - a physical delay while you transition between chords
- Slowly work with each speed bump you notice, giving it the
  attention it needs until you can feel the mental or physical
  hesitation start to relax, and you can feel that you can stroke
  the word with greater ease.
- Be patient with yourself! Smoothing out speed bumps is about slow,
  careful work. Let speed be a byproduct of this careful work.

You can do it!!!

{detailed_word_list}

🐦🥋
"""
            f.write(text)

        if mini_lesson:
            text = f"""Need For Speed Words!
---------------------
{word_list}
"""
            return text
        return text
