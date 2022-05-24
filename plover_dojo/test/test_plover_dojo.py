from unittest import TestCase
from unittest.mock import MagicMock

from plover_dojo.plugins.dojo_test import DojoTest
from plover_dojo.plugins.activity_log import ActivityLog

class TestPloverDojo(TestCase):
    def test_dojo_test_plugin(self):
        DojoTest(MagicMock())

    def test_activity_log_plugin(self):
        ActivityLog(MagicMock())
