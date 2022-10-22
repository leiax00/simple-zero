FROM python:3.9 as builder
MAINTAINER "leiax00@outlook.com"

COPY . /src

FROM python:3.9
MAINTAINER "leiax00@outlook.com"

ENV WORK_DIR="/home/serve"
ENV PATH="${WORK_DIR}:${PATH}"

COPY --from=builder /src/deploy/bash/start_py.sh ${WORK_DIR}/
COPY --from=builder /src/python/app/novel/server ${WORK_DIR}/
COPY --from=builder /src/python/pkg ${WORK_DIR}

WORKDIR $WORK_DIR
EXPOSE 11000

ENTRYPOINT ["sh", "/home/serve/start_py.sh"]
