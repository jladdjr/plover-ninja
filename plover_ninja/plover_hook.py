from plover_ninja.plugins.ninja_test import NinjaTest
from plover_ninja.plugins.ninja_repl import NinjaRepl
from plover_ninja.plugins.stroke_efficiency_log import StrokeEfficiencyLog

import logging
logger = logging.getLogger(__name__)

NINJA_PLUGINS = [NinjaRepl, StrokeEfficiencyLog]


class Main:
    def __init__(self, engine):
        self.engine = engine
        self.ninja_plugins = [cls(engine) for cls in NINJA_PLUGINS]


    def start(self):
        self.engine.hook_connect('stroked', self._on_stroked)
        self.engine.hook_connect('translated', self._on_translated)

    def stop(self):
        self.engine.hook_disconnect('stroked', self._on_stroked)
        self.engine.hook_disconnect('translated', self._on_translated)

    def _on_translated(self, old, new):
        for plugin in self.ninja_plugins:
            plugin.on_translated(old, new)

    def _on_stroked(self, stroke):
        for plugin in self.ninja_plugins:
            plugin.on_stroked(stroke)
