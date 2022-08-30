FROM python:3.9
MAINTAINER "leiax00@outlook.com"

COPY . /app
#COPY ../pkg /app/
WORKDIR /app

EXPOSE 13000

VOLUME /data

RUN pip install -r requirement.txt
CMD ["python", 'app.py']
