from plover_dojo.plugins.dojo_plugin import DojoPlugin

class DojoTest(DojoPlugin):

    def on_translated(self, old, new):
        logger.info(f'Something was translated! {_old} {new}\n')

        with open('/tmp/dojo.txt', 'a') as dojo_log:
            dojo_log.write(f'Something was translated! {_old} {new}\n')

    def on_stroked(self, stroke):
        logger.info(f'Something was stroked! {stroke}\n')

        with open('/tmp/dojo.txt', 'a') as dojo_log:
            dojo_log.write(f'Something was stroked! {stroke}\n')
