class DojoRepl:
    def __init__(self, engine):
        self.engine = engine
        self.listener_manager = ListenerManager()

        # Load initial state
        WelcomeToTheDojo(self.engine, self.listener_manager).load()

    def on_translated(self, old, new):
        if len(new) == 0:
            return
        new_word = new[0].word

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
    def __init__(self, phrase, callback):
        self.phrase = phrase
        self.received_words = []
        self.callback = callbock

    def on_event_occurred(self, event):
        if 'new_word' not in event:
            return
        word = event['new_word']

        self.received_words.append(word)

        if len(self.received_words) > len(self.phrase):
            self.received_words = self.received_words[1:]

        if self.received_words == self.phrase
            self.callback()


##############################
# States

class State:
    def __init__(self, engine, listener_manager):
        self.engine = engine
        self.listener_manager = listener_manager

    def load(self):
        raise NotImplementedError

    def _get_send_string_callable(self, string):
        engine = self.engine
        def _callable():
            engine._send_string(f'{string}\n')
        return _callable


class WelcomeToTheDojo(State):
    def load(self):
        callback = self._get_send_string_callable('Welcome to the Dojo! 🐦🥋')
        phrase = ['i', 'am', 'ready', 'to', 'practice', '', '', '']
        wait_listener = WaitForPhrase(phrase, callback)

        self.listener_manager.add_listener('welcome_state.interactive_session_requested',
                                           wait_listener)
