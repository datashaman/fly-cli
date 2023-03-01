default:

install:
	pip install .

install-dev:
	pip install '.[develop]'

clean:
	rm -rf dist/*

.PHONY: dist
dist:
	python setup.py sdist

test:
	pytest

check: dist
	twine check dist/*

upload: clean dist
	twine upload dist/*
