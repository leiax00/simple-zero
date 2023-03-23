FROM node:lts-alpine3.15 as builder
MAINTAINER "leiax00@outlook.com"

ARG UI_RELATIVE_PATH

COPY . /src
WORKDIR /src/simple-zero-ui
RUN ls -al && npm install -g pnpm && pnpm i && \
    pnpm -F sz-${UI_RELATIVE_PATH} build:${UI_RELATIVE_PATH}

FROM caddy:2.6.2-alpine
MAINTAINER "leiax00@outlook.com"

ARG UI_RELATIVE_PATH

WORKDIR /app

COPY --from=builder /src/simple-zero-ui/apps/${UI_RELATIVE_PATH}/dist /app/
COPY --from=builder /src/deploy/build/sz-${UI_RELATIVE_PATH}/Caddyfile /etc/caddy/Caddyfile
COPY --from=builder /src/deploy/caddy_conf /etc/caddy/conf.d/

EXPOSE 80

RUN ls -al
