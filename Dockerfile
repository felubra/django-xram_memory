FROM node:12-slim as builder

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production

FROM python:3.7-slim

ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/share/nltk_data
# Tell apt-get we're never going to be able to give manual feedback:
ENV DEBIAN_FRONTEND=noninteractive

LABEL author=felipe.lubra@gmail.com

WORKDIR /app

COPY --from=builder /app  .

COPY scripts/download_corpora.py Pipfile* ./

RUN set -ex; \
  pip install pipenv; \
  pip install nltk; \
  python ./download_corpora.py; \
  rm ./download_corpora.py;

RUN set -ex; \
  apt-get update; \
  apt-get -y upgrade; \
  apt-get install poppler-utils libmagic-dev git curl gnupg curl -yq --no-install-recommends; \
  curl -f -L https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb > wkhtmltox.deb; \
  apt-get install ./wkhtmltox.deb -f --no-install-recommends -y; \
  apt-get clean; \
  rm wkhtmltox.deb ; \
  rm -rf /var/lib/apt/lists/;

RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000

USER www-data

ENTRYPOINT ["/app/entrypoint.sh"]