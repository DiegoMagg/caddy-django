FROM python:3.8.3-alpine

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

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

COPY Caddyfile /etc/caddy/Caddyfile
