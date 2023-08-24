VENV_NAME?=venv
PYTHON=venv/bin/python3

$(VENV_NAME)/bin/python3:
	python3 -m venv $(VENV_NAME)

install: venv/bin/python3 requirements.txt
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install -r requirements.txt

run: venv/bin/python3
	${PYTHON} main.py

clean:
	rm -rf $(VENV_NAME)

.PHONY: install run clean
