from datetime import datetime

from plover_dojo.plugins.dojo_plugin import DojoPlugin
from plover_dojo import storage

class ActivityLog(DojoPlugin):

    def __init__(self, engine):
        super().__init__(engine)
        self.first_stroke = None
        self.latest_stroke = None
        self.activity_log = storage.ActivityLog()

    def on_translated(self, old, new):
        pass

    def on_stroked(self, stroke):
        if self.first_stroke is None:
            self.first_stroke = self.latest_stroke = datetime.now()
        else:
            self.latest_stroke = datetime.now()

        duration = self.latest_stroke - self.first_stroke

        total_minutes = self.activity_log.add_activity(1)  # TODO
        with open('/tmp/dojo_activity.txt', 'a') as f:
            f.write(f'Update: Have been writing for {total_minutes} minutes\n')
