APP_RELATIVE_PATH=$(shell a=`basename $$PWD` && echo $$a)
INTERNAL_PROTO_FILES=$(shell find internal -name *.proto)
PKG_FILES = $(shell find ../../pkg -name *.proto)
API_FILES = $(shell cd ../../api/$(APP_RELATIVE_PATH) && find . -name *.proto)
COMMON_FILES = $(shell cd ../../api/common && find . -name *.proto)

.PHONY: init
# init env
init:
	go install google.golang.org/protobuf/cmd/protoc-gen-go
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc
	go install github.com/leiax00/protoc-gen-gin
	go install github.com/gogo/protobuf/protoc-gen-gogo
	go install github.com/favadi/protoc-go-inject-tag
	go install github.com/google/wire/cmd/wire
	go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2

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
	  $(COMMON_FILES) && \
	  protoc-go-inject-tag -input="**/*.pb.go"

	cd ../../api/$(APP_RELATIVE_PATH) && protoc --proto_path=. \
	   --proto_path=../../third_party \
	   --gogo_out=paths=source_relative:. \
	   --gin_out=paths=source_relative:. \
	   $(API_FILES) && \
		 protoc-go-inject-tag -input="**/*.pb.go"
