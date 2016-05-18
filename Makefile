ENV=./env/bin
PATH := node_modules/.bin:$(PATH)
SHELL := /bin/bash
PYTHON=$(ENV)/python
PIP=$(ENV)/pip
MANAGE=$(PYTHON) manage.py

environment:
	virtualenv -p `which python3` --system-site-packages env

delete-environment:
	rm -rf ./env

development:
	$(PIP) install -r requirements/development.txt --upgrade

staging:
	$(PIP) install -r requirements/staging.txt --upgrade

production:
	$(PIP) install -r requirements/production.txt --upgrade

node-modules:
	npm install

build-static:
	gulp build

collect-static: build-static
	$(MANAGE) collectstatic --no-input

# Add eslint?
watch:
	gulp watch-dev

flake8:
	$(ENV)/flake8

migrate:
	$(MANAGE) migrate --no-input

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
