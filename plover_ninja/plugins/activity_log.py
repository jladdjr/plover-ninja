from datetime import datetime

from plover_ninja.plugins.ninja_plugin import NinjaPlugin
from plover_ninja import storage


CHORDING_PAUSED_IN_SECONDS = 5


class ActivityLog(NinjaPlugin):

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
            with open('/tmp/ninja_activity.txt', 'a') as f:
                f.write(f'\n\n-------------------------------\nWelcome back!\n\n')
            return
        else:
            self.previous_stroke = self.latest_stroke
            self.latest_stroke = datetime.now()

        gap_between_strokes = int((self.latest_stroke - self.previous_stroke).total_seconds())

        if gap_between_strokes > CHORDING_PAUSED_IN_SECONDS:
            # register previous activity
            previous_activity = int((self.previous_stroke - self.resumed_chording).total_seconds())
            total_active_seconds = self.activity_log.add_activity(previous_activity)

            with open('/tmp/ninja_activity.txt', 'a') as f:
                f.write(f'\n\nUpdate: Added another {previous_activity} seconds\n')
                f.write(f'Total active minutes: {total_active_seconds // 60}\n\n')

            self.resumed_chording = self.latest_stroke
        else:
            current_active_session_duration = int((self.latest_stroke - self.resumed_chording).total_seconds())
            with open('/tmp/ninja_activity.txt', 'a') as f:
                f.write(f'.')

        # TODO: Capture time that occured at end of plover session
