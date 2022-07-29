from unittest import TestCase
from unittest.mock import MagicMock

from plover_ninja.plugins.ninja_repl import WaitForPhrase

class TestNinjaRepl(TestCase):
    def test_receive_exact_phrase_one_word_at_a_time(self):
        mock_callback = MagicMock()
        phrase = ['To', 'be', 'or', 'not', 'to', 'be']

        wait_for_phrase = WaitForPhrase(phrase, mock_callback)

        # deliver all but the last word
        for word in phrase[:-1]:
            # construct event
            stub_event = {'new_word': word}
            wait_for_phrase.on_event_occurred(stub_event)

            self.assertFalse(mock_callback.run.called)

        stub_event = {'new_word': phrase[-1]}
        wait_for_phrase.on_event_occurred(stub_event)
        mock_callback.run.assert_called_once()

    def test_receive_case_insensitive_equivalent_one_word_at_a_time(self):
        mock_callback = MagicMock()
        phrase = ['To', 'be', 'or', 'not', 'to', 'be']
        delivered_phrase = ['TO', 'be', 'oR', 'NOt', 'To', 'BE']

        wait_for_phrase = WaitForPhrase(phrase, mock_callback)

        # deliver all but the last word
        for word in delivered_phrase[:-1]:
            # construct event
            stub_event = {'new_word': word}
            wait_for_phrase.on_event_occurred(stub_event)

            self.assertFalse(mock_callback.run.called)

        stub_event = {'new_word': delivered_phrase[-1]}
        wait_for_phrase.on_event_occurred(stub_event)
        mock_callback.run.assert_called_once()

    def test_receive_exact_phrase_with_multiple_words_at_a_time(self):
        mock_callback = MagicMock()
        phrase = ['To', 'be', 'or', 'not', 'to', 'be']
        delivered_phrase = ['To be', 'or', 'not to be']

        wait_for_phrase = WaitForPhrase(phrase, mock_callback)

        for word in delivered_phrase[:-1]:
            # construct event
            stub_event = {'new_word': word}
            wait_for_phrase.on_event_occurred(stub_event)

            self.assertFalse(mock_callback.run.called)

        stub_event = {'new_word': delivered_phrase[-1]}
        wait_for_phrase.on_event_occurred(stub_event)
        mock_callback.run.assert_called_once()
