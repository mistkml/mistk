NAME:=groundtruth-mnist

include ../../common.mk

docker-image:
	cp ../../../dist/mistk/mistk*.whl ./
	docker build -t sml-data-plugins/$(NAME) \
		--build-arg "http_proxy=${http_proxy}" \
		--build-arg "https_proxy=${https_proxy}" \
		--build-arg "no_proxy=$(no_proxy)" \
		.

docker-tag: docker-image
	docker tag sml-data-plugins/$(NAME) $(DOCKER_REGISTRY)/sml-data-plugins/$(NAME)
	docker tag sml-data-plugins/$(NAME) $(DOCKER_REGISTRY)/sml-data-plugins/$(NAME):$(VERSION)	

docker-push: docker-tag
	docker push $(DOCKER_REGISTRY)/sml-data-plugins/$(NAME):$(VERSION)

docker-push-latest: docker-tag
	docker push $(DOCKER_REGISTRY)/sml-data-plugins/$(NAME)

deploy: docker-push docker-push-latest
