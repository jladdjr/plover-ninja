from plover_dojo.plugins.dojo_test import DojoTest
from plover_dojo.plugins.activity_log import ActivityLog
from plover_dojo.plugins.stroke_efficiency_log import StrokeEfficiencyLog

import logging
logger = logging.getLogger(__name__)

DOJO_PLUGINS = [DojoTest, ActivityLog, StrokeEfficiencyLog]


class Main:
    def __init__(self, engine):
        self.engine = engine
        self.dojo_plugins = [cls(engine) for cls in DOJO_PLUGINS]


    def start(self):
        self.engine.hook_connect('stroked', self._on_stroked)
        self.engine.hook_connect('translated', self._on_translated)

    def stop(self):
        self.engine.hook_disconnect('stroked', self._on_stroked)
        self.engine.hook_disconnect('translated', self._on_translated)

    def _on_translated(self, old, new):
        for plugin in self.dojo_plugins:
            plugin.on_translated(old, new)

    def _on_stroked(self, stroke):
        for plugin in self.dojo_plugins:
            plugin.on_stroked(stroke)
