from unittest import TestCase
from unittest.mock import MagicMock

from plover_ninja.plugins.ninja_test import NinjaTest

class TestPloverNinja(TestCase):
    def test_ninja_test_plugin(self):
        NinjaTest(MagicMock())
