FROM node:lts-alpine3.15 as builder
MAINTAINER "leiax00@outlook.com"

ARG SOURCE_PREFFIX="ui-main"

COPY . /src
WORKDIR /src

FROM node:lts-alpine3.15
MAINTAINER "leiax00@outlook.com"

ARG SOURCE_PREFFIX="ui-main"
COPY --from=builder /src/${SOURCE_PREFFIX}/ /home/web/
COPY --from=builder /src/deploy/bash/start_web.sh /home/web/

EXPOSE 10000
WORKDIR /home/web

ENTRYPOINT ["./start_app.sh"]
