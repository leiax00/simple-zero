APP_RELATIVE_PATH=$(shell a=`basename $$PWD` && echo $$a)
INTERNAL_PROTO_FILES=$(shell find internal -name *.proto)
PKG_FILES = $(shell find ../../pkg -name *.proto)
API_FILES = $(shell cd ../../api/$(APP_RELATIVE_PATH) && find . -name *.proto)
COMMON_FILES = $(shell cd ../../api/common && find . -name *.proto)

.PHONY: init
# init env
init:
	go get -u google.golang.org/protobuf/cmd/protoc-gen-go
	go get -u google.golang.org/grpc/cmd/protoc-gen-go-grpc
	go get -u github.com/leiax00/protoc-gen-gin
	go get -u github.com/gogo/protobuf/blob/master/protoc-gen-gogo
	go get -u github.com/favadi/protoc-go-inject-tag
	go get -u github.com/google/wire/cmd/wire
	go get -u github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2

.PHONY: wire
# generate wire
wire:
	cd cmd && wire

.PHONY: generate
# generate client code
generate:
	go generate ./...

.PHONY: proto
# generate internal proto struct
proto:
	protoc --proto_path=. \
           --proto_path=../../third_party \
           --proto_path=../../pkg \
           --gogo_out=paths=source_relative:. \
           $(INTERNAL_PROTO_FILES)


.PHONY: proto_pkg
# generate internal proto struct
proto_pkg:
	protoc --proto_path=../../pkg \
           --proto_path=../../third_party \
           --gogo_out=paths=source_relative:../../pkg \
           $(PKG_FILES)

.PHONY: proto_api
# generate internal proto struct
proto_api:
	cd ../../api/common && protoc --proto_path=. \
		  --proto_path=../../third_party \
		  --gogo_out=paths=source_relative:. \
		  --gin_out=paths=source_relative:. \
		  $(COMMON_FILES)
	cd ../../api/$(APP_RELATIVE_PATH) && protoc --proto_path=. \
           --proto_path=../../third_party \
           --gogo_out=paths=source_relative:. \
           --gin_out=paths=source_relative:. \
           $(API_FILES)