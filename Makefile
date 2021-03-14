VIRTUALENV_DIR = .venv
PYTHON_VERSION = 3.8

act:
	act -P ubuntu-latest=ubuntu-builder

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
		python opentunes_api/main.py server --reload --host 0.0.0.0

virtualenv-import:
	. $(VIRTUALENV_DIR)/bin/activate && \
		python opentunes_api/main.py import-tracks 

virtualenv-autoformat:
	. $(VIRTUALENV_DIR)/bin/activate && ./autoformat.sh $$(find opentunes_api/ -name "*.py" -printf "%p ")

virtualenv-lint:
	. $(VIRTUALENV_DIR)/bin/activate && \
		flake8 opentunes_api && \
		mypy opentunes_api

virtualenv-shell:
	. $(VIRTUALENV_DIR)/bin/activate && ipython

virtualenv-test:
	. $(VIRTUALENV_DIR)/bin/activate && pytest

virtualenv-upgrade-requirements:
	. $(VIRTUALENV_DIR)/bin/activate && \
		pur -r requirements.txt && \
		pur -r requirements-dev.txt

virtualenv-makemigrations:
	. $(VIRTUALENV_DIR)/bin/activate && alembic revision --autogenerate

virtualenv-migrate:
	. $(VIRTUALENV_DIR)/bin/activate && alembic upgrade head

virtualenv-clean-db:
	rm -f /tmp/opentunes.sqlite && \
		rm -f alembic/versions/* && \
		$(MAKE) virtualenv-makemigrations && \
		$(MAKE) virtualenv-migrate


readme-convert-markdown-rst:
	. $(VIRTUALENV_DIR)/bin/activate && pandoc --from=markdown --to=rst --output=README.rst README.md

download-stockmusic:
	wget -q -O - https://github.com/wolkenarchitekt/opentunes-stockmusic/archive/master.tar.gz | tar xz opentunes-stockmusic-master/music/ --strip-components=1
