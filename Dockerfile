FROM node:lts-alpine as pre_install

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production

FROM python:3.7-slim-buster as production

ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/share/nltk_data

LABEL author=felipe.lubra@gmail.com

WORKDIR /app

COPY --from=pre_install /app  .

COPY scripts/download_corpora.py Pipfile* ./

RUN set -ex; \
  apt-get update; \
  apt-get install git poppler-utils curl libmagic-dev curl gnupg python3-dev default-libmysqlclient-dev --no-install-recommends -yq; \
  pip install pipenv; \
  pip install nltk; \
  python ./download_corpora.py; \
  rm ./download_corpora.py; \
  curl -f -L https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb > wkhtmltox.deb; \
  apt-get install ./wkhtmltox.deb -f --no-install-recommends -yq; \
  pipenv install --system --deploy ; \
  rm wkhtmltox.deb ; \
  apt-get remove git curl -yq ; \
  apt-get autoclean -yq && apt-get autoremove -yq ; \
  rm -rf /var/lib/apt/lists/;

COPY . .

EXPOSE 8000

USER www-data

ENTRYPOINT ["/app/entrypoint.sh"]

FROM production as development

USER root

RUN set -ex; \
  apt-get update; \
  apt-get install git --no-install-recommends -yq; \
  pipenv install --dev --system --deploy; \
  apt-get remove git -yq; \
  apt-get autoclean -yq && apt-get autoremove -yq ; \
  rm -rf /var/lib/apt/lists/;

USER www-data