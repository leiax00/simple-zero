FROM node:lts-alpine3.15 as builder
MAINTAINER "leiax00@outlook.com"

ARG SOURCE_PREFFIX="ui-main"

COPY . /src
WORKDIR /src

FROM node:lts-alpine3.15
MAINTAINER "leiax00@outlook.com"

ARG SOURCE_PREFFIX="ui-main"
ARG WORK_DIR="/home/web"
COPY --from=builder /src/${SOURCE_PREFFIX}/ ${WORK_DIR}/
COPY --from=builder /src/deploy/bash/start_web.sh ${WORK_DIR}/

EXPOSE 10000
WORKDIR ${WORK_DIR}

ENTRYPOINT ["sh", "/home/web/start_web.sh"]
