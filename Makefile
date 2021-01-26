VIRTUALENV_DIR = .venv
PYTHON_VERSION = 3.8

virtualenv-create:
	python$(PYTHON_VERSION) -m venv $(VIRTUALENV_DIR)
	. $(VIRTUALENV_DIR)/bin/activate && \
		pip install --upgrade pip setuptools && \
		pip install -r requirements.txt && \
        pip install .
	@echo "Activate virtualenv:\n. $(VIRTUALENV_DIR)/bin/activate"

virtualenv-runserver:
	. $(VIRTUALENV_DIR)/bin/activate && \
		uvicorn fastapi_tracks.main:app --reload


virtualenv-autoformat:
	. $(VIRTUALENV_DIR)/bin/activate && ./autoformat.sh **/*.py

readme-convert-markdown-rst:
	. $(VIRTUALENV_DIR)/bin/activate && pandoc --from=markdown --to=rst --output=README.rst README.md
