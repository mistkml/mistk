MODEL_NAME:=atl-mnist-logistic-regression-py38-json

include ../../common.mk

docker-image:
	rm -f ./mistk*.whl
	cp ../../../dist/mistk/mistk*.whl ./
	docker build -t sml-models/$(MODEL_NAME) \
	--build-arg "http_proxy=${http_proxy}" \
	--build-arg "https_proxy=${https_proxy}" \
	--build-arg "no_proxy=$(no_proxy)" \
	.

docker-test: 
	docker run -it --volume /tmp:/tmp --publish 8080:8080 sml-models/$(MODEL_NAME):latest

docker-tag: docker-image
	docker tag sml-models/$(MODEL_NAME) $(DOCKER_REGISTRY)/sml-models/$(MODEL_NAME)
	docker tag sml-models/$(MODEL_NAME) $(DOCKER_REGISTRY)/sml-models/$(MODEL_NAME):$(VERSION)

docker-container:
	docker run -it --publish 8080:8080 --entrypoint /bin/bash sml-models/$(MODEL_NAME):latest


docker-push: docker-tag
	docker push $(DOCKER_REGISTRY)/sml-models/$(MODEL_NAME):$(VERSION)

docker-push-latest: docker-tag
	docker push $(DOCKER_REGISTRY)/sml-models/$(MODEL_NAME):latest

deploy: docker-push
