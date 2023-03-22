FROM golang:1.20.2 AS builder

ARG APP_RELATIVE_PATH
ARG APP_NAME
ARG VERSION

COPY . /src
WORKDIR /src/simple-zero-go/app/${APP_RELATIVE_PATH}

RUN GOPROXY=https://goproxy.cn,direct make build

FROM debian:stable-slim
MAINTAINER "leiax00@outlook.com"

ARG APP_RELATIVE_PATH
COPY --from=builder /src/simple-zero-go/app/${APP_RELATIVE_PATH}/bin /app
COPY --from=builder /src/simple-zero-go/app/${APP_RELATIVE_PATH}/configs /data/conf
WORKDIR /app
EXPOSE 8080
VOLUME /data/conf

CMD ["./cmd", "-conf", "/data/conf"]