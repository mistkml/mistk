include ../agent-common.mk

AGENT_NAME:=atl-test-agent

version:=1.0.0

docker-image:
	cp ../../mistk/dist/mistk/mistk*.whl ./
	docker build -t $(NAMESPACE)/$(AGENT_NAME) \
	--build-arg "http_proxy=${http_proxy}" \
	--build-arg "https_proxy=${https_proxy}" \
	--build-arg "no_proxy=$(no_proxy)" \
	--build-arg "version=$(version)" \
	.

docker-test-1:
	docker run -it --rm --name $(AGENT_NAME)1 --volume /tmp:/tmp --network mistk --publish 8081:8081 $(NAMESPACE)/$(AGENT_NAME)

docker-test-2:
	docker run -it --name $(AGENT_NAME)2 --volume /tmp:/tmp --network mistk --publish 8082:8082 $(NAMESPACE)/$(AGENT_NAME)

docker-tag: docker-image
	docker tag $(NAMESPACE)/$(AGENT_NAME) $(DOCKER_REGISTRY)/$(NAMESPACE)/$(AGENT_NAME)
	docker tag $(NAMESPACE)/$(AGENT_NAME) $(DOCKER_REGISTRY)/$(NAMESPACE)/$(AGENT_NAME):$(version)

docker-push: docker-tag
	docker push $(DOCKER_REGISTRY)/$(NAMESPACE)/$(AGENT_NAME):$(version)

docker-push-latest: docker-tag
	docker push $(DOCKER_REGISTRY)/$(NAMESPACE)/$(AGENT_NAME):latest

deploy: docker-push
