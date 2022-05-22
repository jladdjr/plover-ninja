dev_install:
	plover -s plover_plugins install -e .
dev_uninstall:
	plover -s plover_plugins install dojo-plugin
list_plugins:
	plover -s plover_plugins list
tail_log:
	tail -f /home/jim/.local/share/plover/plover.log
