PLOVER_CMD = "plover"
#PLOVER_CMD = "/Applications/Plover.app/Contents/MacOS/Plover"

dev_install:
	$(PLOVER_CMD) -s plover_plugins install -e .
        #/Applications/Plover.app/Contents/MacOS/Plover
dev_uninstall:
	$(PLOVER_CMD) -s plover_plugins install dojo-plugin
list_plugins:
	$(PLOVER_CMD) -s plover_plugins list
tail_log:
	tail -f /home/jim/.local/share/plover/plover.log
test:
	pytest --pdb plover_dojo/test
venv:
	rm -rf venv
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt
clean:
	#rm -rf venv
	rm -rf plover_dojo.egg-info
	find ./plover_dojo -type d -name __pycache__ -exec rm -rf {} \;
	find ./plover_dojo -type d -name '*.pyc' -exec rm -rf {} \;

clean_db:
	rm ~/.dojo/dojo.db
