NAME:=mistk

UID:=$(shell id -u)
GID:=$(shell id -g)
USER:=$(shell whoami)
VERSION:=$(shell git describe --abbrev=0 --always --tags)
PYTHON:=$(shell which python3.6)

NAMESPACE:=mistk

OUTPUT_BASE_DIR:=/$(NAMESPACE)/$(NAME)

# This needs to be imported from a sub directory.
BASE_DIR:=$(shell pwd)/../
CODEGEN:=docker run --rm -u $(UID):$(GID) -v $(BASE_DIR):/$(NAMESPACE) -w /$(NAMESPACE) swaggerapi/swagger-codegen-cli:2.4.8

.PHONY: help


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: $(NAME) docs dist

clean: ## Remove all build artifacts
	rm -rf gen $(NAME)/model/server $(NAME)/model/client $(NAME)/transform/server $(NAME)/transform/client $(NAME)/evaluation/server $(NAME)/evaluation/client
	rm -rf build test-harness/build docs dist *.egg-info test-harness/*.egg-info sphinx_docs
	find . -name __pycache__ -exec rm -rf {} \;

gen/$(NAME)/model_server: mistk-model-api.yaml
	rm -rf gen/$(NAME)/model_server
	$(CODEGEN) generate -l python-flask -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/model_server -i $(OUTPUT_BASE_DIR)/mistk-model-api.yaml -D packageName=$(NAME).model.server

gen/$(NAME)/transform_server: mistk-transform-api.yaml
	rm -rf gen/$(NAME)/transform_server
	$(CODEGEN) generate -l python-flask -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/transform_server -i $(OUTPUT_BASE_DIR)/mistk-transform-api.yaml -D packageName=$(NAME).transform.server

gen/$(NAME)/evaluation_server: mistk-evaluation-api.yaml
	rm -rf gen/$(NAME)/evaluation_server
	$(CODEGEN) generate -l python-flask -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/evaluation_server -i $(OUTPUT_BASE_DIR)/mistk-evaluation-api.yaml -D packageName=$(NAME).evaluation.server

gen:: gen/$(NAME)_server gen/$(NAME)/transform_server gen/$(NAME)/evaluation_server


$(NAME)/server: gen/$(NAME)/model_server gen/$(NAME)/transform_server gen/$(NAME)/evaluation_server ## Generate the server implementation from the swagger spec
	rm -rf $(NAME)/model/server
	mkdir -p $(NAME)/model/server
	cp -rv gen/$(NAME)/model_server/$(NAME).model.server/* $(NAME)/model/server
	cp -rv gen/$(NAME)/model_server/$(NAME)/model/server/* $(NAME)/model/server

	rm -rf $(NAME)/transform/server
	mkdir -p $(NAME)/transform/server
	cp -rv gen/$(NAME)/transform_server/$(NAME).transform.server/* $(NAME)/transform/server
	cp -rv gen/$(NAME)/transform_server/$(NAME)/transform/server/* $(NAME)/transform/server

	rm -rf $(NAME)/evaluation/server
	mkdir -p $(NAME)/evaluation/server
	cp -rv gen/$(NAME)/evaluation_server/$(NAME).evaluation.server/* $(NAME)/evaluation/server
	cp -rv gen/$(NAME)/evaluation_server/$(NAME)/evaluation/server/* $(NAME)/evaluation/server
	

gen/$(NAME)/model_client: mistk-model-api.yaml
	rm -rf gen/$(NAME)/model_client
	$(CODEGEN) generate -l python -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/model_client -i $(OUTPUT_BASE_DIR)/mistk-model-api.yaml -D packageName=$(NAME).model.client

gen/$(NAME)/transform_client: mistk-transform-api.yaml
	rm -rf gen/$(NAME)/transform_client
	$(CODEGEN) generate -l python -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/transform_client -i $(OUTPUT_BASE_DIR)/mistk-transform-api.yaml -D packageName=$(NAME).transform.client

gen/$(NAME)/evaluation_client: mistk-evaluation-api.yaml
	rm -rf gen/$(NAME)/evaluation_client
	$(CODEGEN) generate -l python -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/evaluation_client -i $(OUTPUT_BASE_DIR)/mistk-evaluation-api.yaml -D packageName=$(NAME).evaluation.client

gen:: gen/$(NAME)/model_client gen/$(NAME)/transform_client gen/$(NAME)/evaluation_client

$(NAME)/client: gen/$(NAME)/model_client gen/$(NAME)/transform_client gen/$(NAME)/evaluation_client ## Generate the client implementations from the swagger spec
	rm -rf $(NAME)/model/client
	mkdir -p $(NAME)/model/client
	cp -rv gen/$(NAME)/model_client/$(NAME).model.client/* $(NAME)/model/client
	cp -rv gen/$(NAME)/model_client/$(NAME)/model/client/* $(NAME)/model/client

	rm -rf mistk/transform/client
	mkdir -p mistk/transform/client
	cp -rv gen/$(NAME)/transform_client/mistk.transform.client/* mistk/transform/client
	cp -rv gen/$(NAME)/transform_client/mistk/transform/client/* mistk/transform/client

	rm -rf mistk/evaluation/client
	mkdir -p mistk/evaluation/client
	cp -rv gen/$(NAME)/evaluation_client/mistk.evaluation.client/* mistk/evaluation/client
	cp -rv gen/$(NAME)/evaluation_client/mistk/evaluation/client/* mistk/evaluation/client
	

$(NAME): $(NAME)/server $(NAME)/client 

dist: $(NAME) docs  $(shell find $(NAME)) test-harness $(shell find . -maxdepth 1 -type f) ## Create a python binary wheel distribution
	rm -rf dist && mkdir dist
	export VERSION=$(VERSION)
	$(PYTHON) setup.py bdist_wheel -d dist/$(NAME)/
	cd test-harness && $(PYTHON) setup.py bdist_wheel  -d ../dist/$(NAME)-test-harness/

install: dist ## Install the python library for the local user
	$(PYTHON) -m pip install $(shell find dist -type f) --user

docker-image: dist ## Create a docker image
	docker build -t $(NAME) \
		--build-arg "http_proxy=${http_proxy}" \
		--build-arg "https_proxy=${https_proxy}" \
		--build-arg "no_proxy=${no_proxy}" \
		.

docker-test: docker-image ## Run the docker image locally to test. 
	docker run -it $(NAME)

sphinx_docs: $(NAME) ## Generate API documentation in the Sphinx format
	rm -rf sphinx_docs
	mkdir -p sphinx_docs
	sphinx-apidoc -o sphinx_docs/ . -F -e -H "MISTK Model Developer API" -V "$(VERSION)" -R "$(VERSION)"
	pushd sphinx_docs && sed -i old '15,17s/\# //' conf.py && make html && popd

swagger_docs:
	rm -rf docs
	$(CODEGEN) generate -l html -o $(OUTPUT_BASE_DIR)/docs/models -i $(OUTPUT_BASE_DIR)/mistk-model-api.yaml -D packageVersion=$(VERSION)
	$(CODEGEN) generate -l html -o $(OUTPUT_BASE_DIR)/docs/models -i $(OUTPUT_BASE_DIR)/mistk-transform-api.yaml -D packageVersion=$(VERSION)
	$(CODEGEN) generate -l html -o $(OUTPUT_BASE_DIR)/docs/models -i $(OUTPUT_BASE_DIR)/mistk-evaluation-api.yaml -D packageVersion=$(VERSION)
docs: swagger_docs ## Generate all documentation
