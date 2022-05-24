class DojoPlugin:
    def __init__(self, engine):
        pass

    def on_translated(self, old, new):
        return NotImplemented

    def on_stroked(self, stroke):
        return NotImplemented
