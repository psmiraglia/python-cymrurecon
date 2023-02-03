SOURCES := setup.py \
	cymrurecon/__init__.py \
	cymrurecon/cymrurecon.py \
	cymrurecon/jobs.py \
	cymrurecon/results.py

default: install

install:
	pip install -e .

flake8:
	flake8 $(SOURCES)

isort-diff:
	isort --diff $(SOURCES)

isort:
	isort $(SOURCES)

style: flake8 isort-diff
