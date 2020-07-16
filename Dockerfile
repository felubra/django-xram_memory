FROM node:lts-alpine as builder

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production

FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/share/nltk_data

LABEL author=felipe.lubra@gmail.com

WORKDIR /app

COPY --from=builder /app  .

COPY scripts/download_corpora.py Pipfile* ./

RUN set -ex; \
  apt-get update; \
  apt-get install git poppler-utils libmagic-dev curl gnupg python3-dev default-libmysqlclient-dev -yq;

RUN set -ex; \
  pip install pipenv; \
  pip install nltk; \
  python ./download_corpora.py; \
  rm ./download_corpora.py; \
  curl -f -L https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb > wkhtmltox.deb; \
  apt-get install ./wkhtmltox.deb -f --no-install-recommends -y; \
  rm wkhtmltox.deb ; \
  rm -rf /var/lib/apt/lists/;

ARG PIPENV_DEV=false
ARG PIPENV_SYSTEM=true

RUN pipenv install --deploy

COPY . .

EXPOSE 8000

USER 1000

ENTRYPOINT ["/app/entrypoint.sh"]