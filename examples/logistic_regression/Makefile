NAME:=scikit-basicmodels
FULLNAME:=scikit-basicmodels

UID:=$(shell id -u)
GID:=$(shell id -g)
USER:=$(shell whoami)
PYTHON:=$(shell which python3.6)

VERSION:=0.0.1
NAMESPACE:=models
VERSION_TAG:=$(addprefix $(NAMESPACE)/,$(FULLNAME)):$(VERSION)
TAG:=$(addprefix $(NAMESPACE)/,$(FULLNAME)):latest

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Remove all build artifacts
	rm -rf build dist setup.cfg *.egg-info
	$(PYTHON) setup.py clean

dist:
	rm -rf dist && mkdir -p dist
	$(PYTHON) setup.py bdist_wheel -d dist/$(NAME)

install: dist
	pip install $(shell find dist -type f) --user

docker-image: dist
	docker build -t $(TAG) --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} --build-arg HTTP_PROXY=${HTTP_PROXY} --build-arg HTTPS_PROXY=${HTTP_PROXY} --build-arg NO_PROXY=${NO_PROXY} --build-arg no_proxy=${NO_PROXY} --file Dockerfile .
