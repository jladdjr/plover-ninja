from unittest import TestCase
from unittest.mock import MagicMock

from plover_ninja.plugins.ninja_test import NinjaTest
from plover_ninja.plugins.activity_log import ActivityLog

class TestPloverNinja(TestCase):
    def test_ninja_test_plugin(self):
        NinjaTest(MagicMock())

    def test_activity_log_plugin(self):
        ActivityLog(MagicMock())
