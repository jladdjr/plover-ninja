PLOVER_CMD = plover
#PLOVER_CMD = /Applications/Plover.app/Contents/MacOS/Plover

install:
	$(PLOVER_CMD) -s plover_plugins install plover-ninja

dev_install:
	$(PLOVER_CMD) -s plover_plugins install -U -e .
	# workaround since using 'Plover -s plover_plugins install'
	# isn't working on Mac OS X
	#/Applications/Plover.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 -m pip install -e .
dev_uninstall:
	$(PLOVER_CMD) -s plover_plugins uninstall plover-ninja
list_plugins:
	$(PLOVER_CMD) -s plover_plugins list
tail_log:
	tail -f /home/jim/.local/share/plover/plover.log
test:
	pytest --pdb plover_ninja/test
venv:
	rm -rf venv
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt
	venv/bin/pip3 install -r requirements_packaging.txt
clean:
	#rm -rf venv
	rm -rf plover_ninja.egg-info
	find ./plover_ninja -type d -name __pycache__ -exec rm -rf {} \;
	find ./plover_ninja -type d -name '*.pyc' -exec rm -rf {} \;

clean_db:
	rm ~/.plover_ninja/ninja.db

package:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*
