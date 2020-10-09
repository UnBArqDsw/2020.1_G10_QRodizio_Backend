SHELL := /bin/bash
.PHONY: all clean install test

all: clean install test

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements_dev.txt
	pip install -r requirements_test.txt

install_test:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements_test.txt

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf htmlcov

coverage:
	coverage run -m pytest
	coverage report
	coverage xml
