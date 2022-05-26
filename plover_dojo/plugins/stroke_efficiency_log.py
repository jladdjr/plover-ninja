from datetime import datetime

from plover_dojo.plugins.dojo_plugin import DojoPlugin
from plover_dojo import storage


CHORDING_PAUSED_IN_SECONDS = 5


class StrokeEfficiencyLog(DojoPlugin):

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
        self.activity_log = storage.ActivityLog()

    def on_translated(self, old, new):
        pass

    def on_stroked(self, stroke):
        if self.resumed_chording is None:
            self.resumed_chording = self.previous_stroke = self.latest_stroke = datetime.now()
            return
        else:
            self.previous_stroke = self.latest_stroke
            self.latest_stroke = datetime.now()

        # time in seconds (expressed as a float; includes fractions of a second)
        gap_between_strokes = (self.latest_stroke - self.previous_stroke).total_seconds()

        if gap_between_strokes > CHORDING_PAUSED_IN_SECONDS:
            # can't accurately determine how long this stroke took
            self.resumed_chording = self.latest_stroke
            return

        # record time it took to make last stroke
        storage.
