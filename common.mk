UID:=$(shell id -u)
GID:=$(shell id -g)
USER:=$(shell whoami)
VERSION:=$(shell git describe --abbrev=0 --always --tags)
PYTHON:=$(shell which python3.6)
NAMESPACE:=mistk

FULLNAME:=$(if $(FULLNAME),$(FULLNAME),$(NAME))

API:=$(addsuffix -api.yaml,$(NAME))
OUTPUT_BASE_DIR:=/$(NAMESPACE)/$(FULLNAME)
YAML_FILE=$(OUTPUT_BASE_DIR)/$(API)

# This needs to be imported from a sub directory. 
BASE_DIR:=$(shell pwd)/../
CODEGEN:=docker run --rm -u $(UID):$(GID) -v $(BASE_DIR):/mistk -w /mistk swaggerapi/swagger-codegen-cli:v2.3.1

