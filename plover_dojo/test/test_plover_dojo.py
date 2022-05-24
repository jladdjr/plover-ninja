from unittest import TestCase
from unittest.mock import MagicMock

from plover_dojo.plugins.dojo_test import DojoTest

class TestPloverDojo(TestCase):
    def test_plugins(self):
        DojoTest(MagicMock())
