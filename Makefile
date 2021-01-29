VIRTUALENV_DIR = .venv
PYTHON_VERSION = 3.8

act:
	act

virtualenv-create:
	python$(PYTHON_VERSION) -m venv $(VIRTUALENV_DIR)
	. $(VIRTUALENV_DIR)/bin/activate && \
		pip install --upgrade pip setuptools && \
		pip install -r requirements.txt && \
		pip install -r requirements-dev.txt && \
        pip install -e .
	@echo "Activate virtualenv:\n. $(VIRTUALENV_DIR)/bin/activate"

virtualenv-runserver:
	. $(VIRTUALENV_DIR)/bin/activate && \
		python opentunes_api/main.py server

virtualenv-import:
	. $(VIRTUALENV_DIR)/bin/activate && \
		python opentunes_api/main.py import-tracks music/

virtualenv-autoformat:
	. $(VIRTUALENV_DIR)/bin/activate && ./autoformat.sh **/*.py

virtualenv-shell:
	. $(VIRTUALENV_DIR)/bin/activate && ipython

virtualenv-test:
	. $(VIRTUALENV_DIR)/bin/activate && pytest

readme-convert-markdown-rst:
	. $(VIRTUALENV_DIR)/bin/activate && pandoc --from=markdown --to=rst --output=README.rst README.md

download-stockmusic:
	wget -q -O - https://github.com/wolkenarchitekt/opentunes-stockmusic/archive/master.tar.gz | tar xz opentunes-stockmusic-master/music/ --strip-components=1
