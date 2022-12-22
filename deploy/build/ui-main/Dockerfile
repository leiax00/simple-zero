FROM node:lts-alpine3.15 as builder
MAINTAINER "leiax00@outlook.com"

ARG SOURCE_PREFFIX="ui-main"

COPY ./simple-zero-ui /code
COPY ./deploy/build/ui-main/Caddyfile /code/Caddyfile
WORKDIR /code
RUN ls -al && npm install -g pnpm && pnpm i && pnpm -F sz-main build:main

FROM caddy:2.6.2-alpine
MAINTAINER "leiax00@outlook.com"

ARG SOURCE_PREFFIX="ui-main"
ARG WORK_DIR="/home/serve"
COPY --from=builder /code/apps/main/dist ${WORK_DIR}/
COPY --from=builder /code/Caddyfile /etc/caddy/Caddyfile

EXPOSE 10000
WORKDIR ${WORK_DIR}
RUN ls -al
