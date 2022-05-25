from datetime import datetime

from plover_dojo.plugins.dojo_plugin import DojoPlugin
from plover_dojo import storage


CHORDING_PAUSED_IN_SECONDS = 5


class ActivityLog(DojoPlugin):

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
            with open('/tmp/dojo_activity.txt', 'a') as f:
                f.write(f'\n\n-------------------------------\nWelcome back!\n\n')
            return
        else:
            self.previous_stroke = self.latest_stroke
            self.latest_stroke = datetime.now()

        gap_between_strokes = int((self.latest_stroke - self.previous_stroke).total_seconds())

        if gap_between_strokes > CHORDING_PAUSED_IN_SECONDS:
            # register previous activity if it's greater than a minute
            previous_activity = int((self.previous_stroke - self.resumed_chording).total_seconds())
            if previous_activity > 60:
                # TODO: Keep track of partial minutes
                # only add up activity is it was at least a minute long
                previous_activity_in_min = previous_activity // 60
                total_active_minutes = self.activity_log.add_activity(previous_activity_in_min)

                with open('/tmp/dojo_activity.txt', 'a') as f:
                    f.write(f'\n\nUpdate: Added another {previous_activity_in_min} minutes\n')
                    f.write(f'Total active minutes: {total_active_minutes}\n\n')
            else:
                total_active_minutes = self.activity_log.add_activity(1)
                with open('/tmp/dojo_activity.txt', 'a') as f:
                    f.write(f'\n\nPrevious chording session less than a minute, recording a minute anyways\n')
                    f.write(f'Total active minutes: {total_active_minutes}\n\n')

            self.resumed_chording = self.latest_stroke
        else:
            current_active_session_duration = int((self.latest_stroke - self.resumed_chording).total_seconds())
            with open('/tmp/dojo_activity.txt', 'a') as f:
                f.write(f'.')

        # TODO: Capture time that occured at end of plover session
