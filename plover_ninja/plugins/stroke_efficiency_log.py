
from pathlib import Path
from datetime import datetime

from plover_ninja.lessons.make_a_new_friend import MakeANewFriend
from plover_ninja.lessons.need_for_speed import NeedForSpeed
from plover_ninja.lessons.remember_me import RememberMe
from plover_ninja.plugins.ninja_plugin import NinjaPlugin
from plover_ninja import storage


CHORDING_PAUSED_IN_SECONDS = 5


class StrokeEfficiencyLog(NinjaPlugin):

    def __init__(self, engine):
        """
        resumed_chording - beginning of active typing, resets after a noticeable pause
        previous_stroke - literally, when the last stroke was made
        latest_stroke - _this_ stroke that just happened
        """
        super().__init__(engine)
        self.resumed_chording = None
        self.previous_stroke = None
        self.latest_stroke = None
        self.stroke_efficiency_log = storage.StrokeEfficiencyLog()
        self.words_written_this_session = 0

        with open(Path(storage.TEMP_DIR) / 'ninja-stroke-efficiency.txt', 'a', encoding='utf-8') as f:
            f.write(f'Stroke Efficiency Log is up and running! 🎉\n')

        # TODO: Move lesson creation somewhere else?
        # Create a lesson!
        MakeANewFriend().make_lesson()
        RememberMe().make_lesson()
        NeedForSpeed().make_lesson()


    def _log_efficiency_report(self):
        efficiency_map = self.stroke_efficiency_log.get_average_speed_and_frequency_for_stroked_words()

        with open(Path(storage.TEMP_DIR) / 'ninja-stroke-efficiency.txt', 'a', encoding='utf-8') as f:
            f.write('\n----------------------------------\n')
            f.write('New stroke efficiency results! 🎉\n\n')
            for word, _, avg_stroke_duration in efficiency_map:
                f.write(f'{word} => {avg_stroke_duration}\n')
            f.write('\n')


    def on_translated(self, old, new):
        if len(new) == 0:
            return

        word = new[0].word

        if self.resumed_chording is None:
            self.resumed_chording = self.previous_stroke = self.latest_stroke = datetime.now()
            return
        else:
            self.previous_stroke = self.latest_stroke
            self.latest_stroke = datetime.now()

        self.words_written_this_session += 1

        # time in seconds (expressed as a float; includes fractions of a second)
        gap_between_strokes = (self.latest_stroke - self.previous_stroke).total_seconds()

        if gap_between_strokes > CHORDING_PAUSED_IN_SECONDS:
            # can't accurately determine how long this stroke took
            self.resumed_chording = self.latest_stroke
            return

        # record time it took to make last stroke
        self.stroke_efficiency_log.add_stroke(word, gap_between_strokes)
        with open(Path(storage.TEMP_DIR) / 'ninja-stroke-efficiency.txt', 'a', encoding='utf-8') as f:
            f.write(f'Stroked {word} in {gap_between_strokes:.2f}\n')

    def on_stroked(self, stroke):
        pass
