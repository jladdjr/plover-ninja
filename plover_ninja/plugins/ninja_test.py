
import logging
import tempfile
from pathlib import Path

from plover_ninja.plugins.ninja_plugin import NinjaPlugin

logger = logging.getLogger(__name__)

TEMP_DIR = tempfile.gettempdir()

class NinjaTest(NinjaPlugin):

    def on_translated(self, old, new):
        logger.info(f'Something was translated! {old} {new}\n')

        with open(Path(TEMP_DIR) / 'ninja.txt', 'a', encoding='utf-8') as ninja_log:
            ninja_log.write(f'Something was translated! {old} {new}\n')

    def on_stroked(self, stroke):
        logger.info(f'Something was stroked! {stroke}\n')

        with open(Path(TEMP_DIR) / 'ninja.txt', 'a', encoding='utf-8') as ninja_log:
            ninja_log.write(f'Something was stroked! {stroke}\n')
