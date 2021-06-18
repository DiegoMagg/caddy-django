FROM python:3.9.0-alpine3.12

LABEL maintainer = "Diego Magalhães <dmlmagal@gmail.com>"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD Pipfile /app/Pipfile
ADD Pipfile.lock /app/Pipfile.lock

RUN pip3 install --no-cache-dir --upgrade pipenv pip && rm -rf /root/.cache/*
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    musl-dev \
    linux-headers \
    && apk add postgresql-dev --no-cache \
    && pipenv install --three \
  && rm -rf /root/.cache/* \
  && apk del .build-deps

ADD . /app
