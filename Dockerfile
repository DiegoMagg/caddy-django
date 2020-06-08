FROM python:3.8.3-alpine

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

LABEL maintainer = "Diego Magalhães <dmlmagal@gmail.com>"

RUN apk add --update \
  build-base \
  libffi-dev \
  libpq \
  libressl-dev \
  libxml2 \
  libxml2-dev \
  libxslt \
  libxslt-dev \
  linux-headers \
  postgresql-dev \
  jpeg-dev \
  zlib-dev \
  freetype-dev \
  lcms-dev \
  libwebp-dev \
  harfbuzz-dev \
  fribidi-dev \
  && rm -rf /var/cache/apk/*

WORKDIR /app
RUN pip3 install --no-cache-dir --upgrade pipenv pip && rm -rf /root/.cache/*
ADD Pipfile /app/Pipfile
ADD Pipfile.lock /app/Pipfile.lock

RUN pipenv install --three \
&& rm -rf /root/.cache/*
ADD . /app
