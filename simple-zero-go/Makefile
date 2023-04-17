GOPATH:=$(shell go env GOPATH)
HUB_URI=$(shell echo hub.leiax00.cn)
HUB_REPO=$(shell echo leiax00)
VERSION=$(shell git describe --tags --always)
APP_RELATIVE_PATH=$(shell a=`basename $$PWD` && echo $$a)
INTERNAL_PROTO_FILES=$(shell find internal -name *.proto)
PKG_FILES = $(shell find ../../pkg -name *.proto)
API_FILES = $(shell cd ../../api/$(APP_RELATIVE_PATH) && find . -name *.proto)
COMMON_FILES = $(shell cd ../../api/common && find . -name *.proto)
APP_NAME=$(shell echo sz-$(APP_RELATIVE_PATH))
DOCKER_IMAGE=$(shell echo $(HUB_URI)/$(HUB_REPO)/$(APP_NAME):$(VERSION))
DOCKER_PLATFORM=linux/arm64,linux/amd64
PLATFORM_ACTION=push

.PHONY: init
# init env
init:
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
	go install github.com/leiax00/protoc-gen-gin@latest
	go install github.com/gogo/protobuf/protoc-gen-gogo@latest
	go install github.com/favadi/protoc-go-inject-tag@latest
	go install github.com/google/wire/cmd/wire@latest
	go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2@latest

.PHONY: wire
# generate wire
wire:
	cd cmd && wire

.PHONY: generate
# generate client code
generate:
	go generate ./...

.PHONY: proto_internal
# generate internal proto struct
proto_internal:
	protoc --proto_path=. \
           --proto_path=../../third_party \
           --proto_path=../../pkg \
           --go_out=paths=source_relative:. \
           $(INTERNAL_PROTO_FILES)


.PHONY: proto_common
# generate common proto struct
proto_common:
	# generate pkg proto struct
	protoc --proto_path=../../pkg \
		   --proto_path=../../third_party \
		   --gogo_out=paths=source_relative:../../pkg \
		   $(PKG_FILES)

	# generate common proto struct
	cd ../../api/common && protoc --proto_path=. \
	  --proto_path=../../third_party \
	  --gogo_out=paths=source_relative:. \
	  --gin_out=paths=source_relative:. \
	  $(COMMON_FILES) && \
	  protoc-go-inject-tag -input="**/*.pb.go"


.PHONY: proto_api
# generate serve api proto struct
proto_api:
	cd ../../api/$(APP_RELATIVE_PATH) && protoc --proto_path=. \
	   --proto_path=../../third_party \
	   --gogo_out=paths=source_relative:. \
	   --gin_out=paths=source_relative:. \
	   $(API_FILES) && \
		 protoc-go-inject-tag -input="**/*.pb.go"

.PHONY: proto
# generate all proto struct
proto: proto_internal proto_common proto_api

.PHONY: build
# build
build:
	mkdir -p bin/ && go mod tidy && go build -ldflags \
		"-X main.Version=$(VERSION) -X main.Name=$(APP_NAME)" \
		 -o ./bin/ ./...

.PHONY: all
# generate all
all: wire proto build

.PHONY: docker
# generate docker image
docker:
	cd ../../.. && docker build \
		-f deploy/build/docker/Dockerfile_go \
		--build-arg APP_RELATIVE_PATH=$(APP_RELATIVE_PATH) \
		--build-arg VERSION=$(VERSION) \
		-t $(DOCKER_IMAGE) .

.PHONY: docker-multi
# generate multiple platform docker image
docker-multi:
	cd ../../.. && docker buildx build \
    		-f deploy/build/docker/Dockerfile_go \
    		--build-arg RELATIVE_PATH=$(APP_RELATIVE_PATH) \
    		--build-arg VERSION=$(VERSION) \
    		--platform=$(DOCKER_PLATFORM) \
    		--progress=plain \
    		-t $(DOCKER_IMAGE) . --$(PLATFORM_ACTION)

# show help
help:
	@echo ''
	@echo 'Usage:'
	@echo ' make [target]'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
	helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "\033[36m%-22s\033[0m %s\n", helpCommand,helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help