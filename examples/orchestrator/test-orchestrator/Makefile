include ../orchestrator-common.mk

MODEL_NAME:=atl-test-orchestrator

version:=1.0.0

docker-image:
	cp ../../mistk/dist/mistk/mistk*.whl ./
	docker build -t sml-orchestrators/$(MODEL_NAME) \
	--build-arg "http_proxy=${http_proxy}" \
	--build-arg "https_proxy=${https_proxy}" \
	--build-arg "no_proxy=$(no_proxy)" \
	--build-arg "version=$(version)" \
	.

docker-network:
	docker network create --driver bridge mistk

docker-test:
	docker run -it --rm --name $(MODEL_NAME) --volume /tmp:/tmp --network mistk --publish 8080:8080 sml-orchestrators/$(MODEL_NAME)

docker-tag: docker-image
	docker tag sml-orchestrators/$(MODEL_NAME) $(DOCKER_REGISTRY)/sml-orchestrators/$(MODEL_NAME)
	docker tag sml-orchestrators/$(MODEL_NAME) $(DOCKER_REGISTRY)/sml-orchestrators/$(MODEL_NAME):$(version)

docker-push: docker-tag
	docker push $(DOCKER_REGISTRY)/sml-orchestrators/$(MODEL_NAME):$(version)

docker-push-latest: docker-tag
	docker push $(DOCKER_REGISTRY)/sml-orchestrators/$(MODEL_NAME):latest

deploy: docker-push
