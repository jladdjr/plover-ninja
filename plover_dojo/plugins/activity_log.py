from datetime import datetime

from plover_dojo.plugins.dojo_plugin import DojoPlugin

class ActivityLog(DojoPlugin):

    def __init__(self, engine):
        super().__init__(engine)
        self.first_stroke = None
        self.latest_stroke = None

    def on_translated(self, old, new):
        pass

    def on_stroked(self, stroke):
        if self.first_stroke is None:
            self.first_stroke = self.latest_stroke = datetime.now()
        else:
            self.latest_stroke = datetime.now()

        duration = self.latest_stroke - self.first_stroke
        with open('/tmp/dojo_activity.txt', 'a') as f:
            f.write(f'Update: Have been writing for {duration.seconds} seconds\n')

