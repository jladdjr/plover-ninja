from datetime import date, timedelta

from plover_ninja.plugins.ninja_plugin import NinjaPlugin
from plover_ninja.lessons.need_for_speed import NeedForSpeed
from plover_ninja.lessons.make_a_new_friend import MakeANewFriend
from plover_ninja.storage import get_daily_number_of_strokes


class NinjaRepl(NinjaPlugin):
    def __init__(self, engine):
        self.engine = engine
        self.listener_manager = ListenerManager()

        # Load initial state
        WelcomeToNinjaTraining(self.engine, self.listener_manager).load()

    def on_translated(self, old, new):
        if len(new) == 0:
            return
        new_word = new[0].word

        if new_word is None:
            return
        new_word = new_word.lower()

        event = {'new_word': new_word}
        self.listener_manager.send_event_to_listeners(event)


class ListenerManager:
    def __init__(self):
        self.listeners = {}
        self.permanent_listeners = {}

    def clear_listeners(self):
        self.listeners = {}

    def add_listener(self, listener_name, listener):
        self.listeners[listener_name] = listener

    def add_permanent_listener(self, listener_name, listener):
        self.permanent_listeners[listener_name] = listener

    def remove_listener(self, listener_name):
        del self.listeners[listener_name]

    def send_event_to_listeners(self, event_dict):
        for listener in self.permanent_listeners.values():
            listener.on_event_occurred(event_dict)

        for listener in self.listeners.values():
            listener.on_event_occurred(event_dict)


##############################
# Listeners

class WaitForPhrase:
    """WaitForPhrase waits for a *case-sensitive* phrase!"""
    def __init__(self, phrase, callback):
        self.phrase = phrase
        self.received_words = []
        self.callback = callback

    def on_event_occurred(self, event):
        if 'new_word' not in event:
            return
        word = event['new_word']

        self.received_words.append(word)

        if len(self.received_words) > len(self.phrase):
            self.received_words = self.received_words[1:]

        if self.received_words == self.phrase:
            self.callback.run()


##############################
# Callbacks

class GreetingCallback:
    def __init__(self, engine, mini_lesson=True):
        self.engine = engine
        self.mini_lesson = mini_lesson

    def run(self):
        #self.engine._send_string(f'Howdy!🐦🥋\n')

        lesson_text = MakeANewFriend().make_lesson(mini_lesson=self.mini_lesson)
        self.engine._send_string(lesson_text)

        self.engine._send_string('\n')

        lesson_text = NeedForSpeed().make_lesson(mini_lesson=self.mini_lesson)
        self.engine._send_string(lesson_text)

class StatsCallback:
    def __init__(self, engine, days=30):
        self.engine = engine
        self.days = days

    def run(self):
        stats_text = self.get_stats_content(self.days)
        for line in stats_text:
            self.engine._send_string(f'{line}\n')

    def get_stats_content(self, days):
        date_to_stroke_count_map = get_daily_number_of_strokes()

        # build custom list that:
        # - has entries for each day (including 0 if needed)
        # - only goes back `days`
        date_to_stroke_stats_list = []

        today = date.today()
        for i in range(0, days):
            curr_date = today - timedelta(days=i)
            curr_date_str = curr_date.strftime('%Y-%m-%d')

            num_strokes = date_to_stroke_count_map.get(curr_date_str, 0)
            date_to_stroke_stats_list.append((curr_date_str, num_strokes))

        max_stroke_count = max(strokes for _, strokes in date_to_stroke_stats_list)
        stroke_count_width = len(str(max_stroke_count))

        lines = []
        lines.append(f'{"Date":<13} {"# Words":<{stroke_count_width}}')
        for d, num_strokes in date_to_stroke_stats_list:
            lines.append(f'{d:<13} {num_strokes:<{stroke_count_width}}')
        return lines


##############################
# States

class State:
    def __init__(self, engine, listener_manager):
        self.engine = engine
        self.listener_manager = listener_manager

    def load(self):
        raise NotImplementedError


class WelcomeToNinjaTraining(State):
    def load(self):
        phrase = ['i', 'am', 'ready', 'to', 'practice', '', '', '']
        callback = GreetingCallback(self.engine, mini_lesson=True)
        wait_listener = WaitForPhrase(phrase, callback)

        self.listener_manager.add_listener('welcome_state.interactive_session_requested',
                                           wait_listener)

        phrase = ['i', 'am', 'ready', 'to', 'practice', 'with', 'data', '', '', '']
        callback = GreetingCallback(self.engine, mini_lesson=False)
        wait_listener = WaitForPhrase(phrase, callback)

        self.listener_manager.add_listener('welcome_state.interactive_session_requested_with_details',
                                           wait_listener)

        phrase = ['show', 'stats', '', '', '']
        callback = StatsCallback(self.engine, days=10)
        wait_listener = WaitForPhrase(phrase, callback)

        self.listener_manager.add_listener('welcome_state.show_stats_for_ten_days',
                                           wait_listener)

        phrase = ['show', 'week', '', '', '']
        callback = StatsCallback(self.engine, days=7)
        wait_listener = WaitForPhrase(phrase, callback)

        self.listener_manager.add_listener('welcome_state.show_stats_for_week',
                                           wait_listener)

        phrase = ['show', 'month', '', '', '']
        callback = StatsCallback(self.engine, days=30)
        wait_listener = WaitForPhrase(phrase, callback)

        self.listener_manager.add_listener('welcome_state.show_stats_for_month',
                                           wait_listener)
