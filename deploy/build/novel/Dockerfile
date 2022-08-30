FROM python:3.9 as builder
MAINTAINER "leiax00@outlook.com"

ARG SOURCE_PREFFIX="python"

COPY . /src

FROM python:3.9
MAINTAINER "leiax00@outlook.com"

ARG SOURCE_PREFFIX="python"

COPY --from=builder /src/${SOURCE_PREFFIX}/app/novel/server /app
COPY --from=builder /src/${SOURCE_PREFFIX}/pkg /app
WORKDIR /app

EXPOSE 13000

VOLUME /data

RUN pip install -r requirement.txt
CMD ["python", "app.py"]
