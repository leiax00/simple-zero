APP_VERSION=v0.1.0
APP_NAME=ui-main
APP_PORT=10000
DOCKER_IMAGE=$(shell echo leiax00/$(APP_NAME):$(APP_VERSION))

.PHONY: dockerImage
dockerImage:
	cd .. && docker build -f deploy/build/${APP_NAME}/Dockerfile -t $(DOCKER_IMAGE) .

.PHONY: dockerRun
dockerRun:
	docker run --name $(APP_NAME) -d -p $(APP_PORT):$(APP_PORT) $(DOCKER_IMAGE)
