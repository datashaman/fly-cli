default:

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

.PHONY: dist
dist:
	python setup.py sdist

test:
	pytest

check: dist
	twine check dist/*

upload: dist
	twine upload dist/*
