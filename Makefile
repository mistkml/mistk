NAME:=mistk

include ../utils/common.mk

.PHONY: help


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: $(NAME) docs dist

clean: ## Remove all build artifacts
	$(PYTHON) setup.py clean
	rm -rf gen $(NAME)/model/server $(NAME)/model/client $(NAME)/transform/server $(NAME)/transform/client
	rm -rf build test-harness/build docs dist *.egg-info test-harness/*.egg-info sphinx_docs
	find . -name __pycache__ -exec rm -rf {} \;

../smlcore/sml-api.yaml:
	cd ../smlcore && $(MAKE) sml-api.yaml


gen/$(NAME)/model_server: $(API) ../smlcore/sml-api.yaml
	rm -rf gen/$(NAME)/model_server
	$(CODEGEN) generate -l python-flask -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/model_server -i $(YAML_FILE) -D packageName=$(NAME).model.server	

gen/$(NAME)/transform_server: $(API) ../smlcore/sml-api.yaml
	rm -rf gen/$(NAME)/transform_server	
	$(CODEGEN) generate -l python-flask -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/transform_server -i $(OUTPUT_BASE_DIR)/transform-api.yaml -D packageName=$(NAME).transform.server

gen:: gen/$(NAME)_server gen/$(NAME)/transform_server


$(NAME)/server: gen/$(NAME)/model_server gen/$(NAME)/transform_server
	rm -rf $(NAME)/model/server
	mkdir -p $(NAME)/model/server
	cp -rv gen/$(NAME)/model_server/$(NAME).model.server/* $(NAME)/model/server
	cp -rv gen/$(NAME)/model_server/$(NAME)/model/server/* $(NAME)/model/server
	
	rm -rf $(NAME)/transform/server
	mkdir -p $(NAME)/transform/server	
	cp -rv gen/$(NAME)/transform_server/$(NAME).transform.server/* $(NAME)/transform/server
	cp -rv gen/$(NAME)/transform_server/$(NAME)/transform/server/* $(NAME)/transform/server
	

gen/$(NAME)/model_client: $(API)
	rm -rf gen/$(NAME)/model_client
	$(CODEGEN) generate -l python -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/model_client -i $(YAML_FILE) -D packageName=$(NAME).model.client

gen/$(NAME)/transform_client: $(API)
	rm -rf gen/$(NAME)/transform_client
	$(CODEGEN) generate -l python -o $(OUTPUT_BASE_DIR)/gen/$(NAME)/transform_client -i $(OUTPUT_BASE_DIR)/transform-api.yaml -D packageName=$(NAME).transform.client

gen:: gen/$(NAME)/model_client gen/$(NAME)/transform_client

$(NAME)/client: gen/$(NAME)/model_client gen/$(NAME)/transform_client
	rm -rf $(NAME)/model/client
	mkdir -p $(NAME)/model/client
	cp -rv gen/$(NAME)/model_client/$(NAME).model.client/* $(NAME)/model/client
	cp -rv gen/$(NAME)/model_client/$(NAME)/model/client/* $(NAME)/model/client
	
	rm -rf mistk/transform/client
	mkdir -p mistk/transform/client
	cp -rv gen/$(NAME)/transform_client/mistk.transform.client/* mistk/transform/client
	cp -rv gen/$(NAME)/transform_client/mistk/transform/client/* mistk/transform/client

$(NAME): $(NAME)/server $(NAME)/client

sphinx_docs:
	rm -rf sphinx_docs
	mkdir -p sphinx_docs
	sphinx-apidoc -o sphinx_docs/ . -F -e -H "MISTK Model Developer API" -V "$(VERSION)" -R "$(VERSION)" -A "Asif Dipon, Andrew Shilliday, Jason Isabel, Tom Damiano"
	pushd sphinx_docs && make latexpdf && popd

docs: $(API) ## Generate documentation for the API
	rm -rf docs
	$(CODEGEN) generate -l html -o $(OUTPUT_BASE_DIR)/docs -i $(YAML_FILE) -D packageVersion=$(VERSION)

dist: $(NAME) docs  $(shell find $(NAME)) test-harness $(shell find . -maxdepth 1 -type f)
	rm -rf dist && mkdir dist
	$(PYTHON) setup.py bdist_wheel -d dist/$(NAME)/
	cd test-harness && $(PYTHON) setup.py bdist_wheel  -d ../dist/$(NAME)-test-harness

docker-image: dist
	docker build -t mistk \
		--build-arg "http_proxy=$http_proxy" \
		--build-arg "https_proxy=$https_proxy" \
		--build-arg "no_proxy=$no_proxy" \
		.

install: dist
	$(PYTHON) -m pip install $(shell find dist -type f) --user

upload: dist
	twine upload --skip-existing -u $(PYPI_USER) -p $(PYPI_PASSWORD) --repository-url $(PYPI_LOCATION) $(shell find dist -type f)

