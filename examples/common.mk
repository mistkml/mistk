UID:=$(shell id -u)
GID:=$(shell id -g)
USER:=$(shell whoami)
VERSION:=$(shell git describe --abbrev=0 --always --tags)
PYTHON:=$(shell which python3.6)
FULLNAME:=$(if $(FULLNAME),$(FULLNAME),$(NAME))

DOCKER_REGISTRY:=docker-registry:5000/sml/streamlinedml
