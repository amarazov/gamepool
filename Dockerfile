FROM python:3.6-alpine

RUN apk update && apk upgrade

RUN apk add --no-cache curl pkgconfig openssl-dev libffi-dev musl-dev make gcc

RUN adduser -D gamepool

WORKDIR /home/gamepool

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql


COPY app app
COPY migrations migrations
COPY gamepool.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP gamepool.py

RUN chown -R gamepool:gamepool ./
USER gamepool

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
