import logging

from plover_ninja.plugins.ninja_plugin import NinjaPlugin

logger = logging.getLogger(__name__)

class NinjaTest(NinjaPlugin):

    def on_translated(self, old, new):
        logger.info(f'Something was translated! {old} {new}\n')

        with open('/tmp/ninja.txt', 'a') as ninja_log:
            ninja_log.write(f'Something was translated! {old} {new}\n')

    def on_stroked(self, stroke):
        logger.info(f'Something was stroked! {stroke}\n')

        with open('/tmp/ninja.txt', 'a') as ninja_log:
            ninja_log.write(f'Something was stroked! {stroke}\n')
