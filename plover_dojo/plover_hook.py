import logging
logger = logging.getLogger(__name__)

class Main:
    def __init__(self, engine):
        self.engine = engine

    def start(self):
        self.engine.hook_connect('stroked', self._on_stroked)
        self.engine.hook_connect('translated', self._on_translated)

    def stop(self):
        self.engine.hook_disconnect('stroked', self._on_stroked)
        self.engine.hook_disconnect('translated', self._on_translated)

    def _on_translated(self, _old, new):
        logger.info(f'Something was translated! {_old} {new}\n')

        with open('/tmp/dojo.txt', 'a') as dojo_log:
            dojo_log.write(f'Something was translated! {_old} {new}\n')

    def _on_stroked(self, stroke):
        logger.info(f'Something was stroked! {stroke}\n')

        with open('/tmp/dojo.txt', 'a') as dojo_log:
            dojo_log.write(f'Something was stroked! {stroke}\n')


