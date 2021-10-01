NAME:=atl-mnist-logistic-regression

include ../../common.mk

docker-image:
	cp ../../../dist/mistk/mistk*.whl ./
	docker build -t sml-models/$(NAME) \
    	--build-arg "http_proxy=${http_proxy}" \
    	--build-arg "https_proxy=${https_proxy}" \
    	--build-arg "no_proxy=$(no_proxy)" \
    	.

docker-test: 
	docker run -it --volume /tmp:/tmp --publish 8080:8080 sml-models/$(NAME)

docker-tag: docker-image
	docker tag sml-models/$(NAME) $(DOCKER_REGISTRY)/sml-models/$(NAME)
	docker tag sml-models/$(NAME) $(DOCKER_REGISTRY)/sml-models/$(NAME):$(VERSION)

docker-push: docker-tag
	docker push $(DOCKER_REGISTRY)/sml-models/$(NAME):$(VERSION)

docker-push-latest: docker-tag
	docker push $(DOCKER_REGISTRY)/sml-models/$(NAME):latest

deploy: docker-push docker-push-latest
