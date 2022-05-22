class Extension:
  def __init__(self, engine):
    # Called once to initialize an instance which lives until Plover exits.
    pass

  def start(self):
    # Called to start the extension or when the user enables the extension.
    # It can be used to start a new thread for example.
    with open('/tmp/dojo.log', 'a') as dojo_log:
        dojo_log.write('plover-dojo is running!')

  def stop(self):
    # Called when Plover exits or the user disables the extension.
    pass
