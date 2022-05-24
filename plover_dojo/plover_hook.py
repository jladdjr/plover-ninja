from plugins.dojo_test import DojoTest

import logging
logger = logging.getLogger(__name__)

DOJO_PLUGINS = [DojoTest]


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
