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
  # Atualize as dependências de sistema
  apt-get update; \
  apt-get install git poppler-utils curl libmagic-dev curl gnupg python3-dev default-libmysqlclient-dev --no-install-recommends -yq; \
  # Instale o pipenv, o nltk e seus datasets
  pip install pipenv; \
  pip install nltk; \
  python ./download_corpora.py; \
  rm ./download_corpora.py; \
  # Baixe e instale o wkhtml
  curl -f -L https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb > wkhtmltox.deb; \
  apt-get install ./wkhtmltox.deb -f --no-install-recommends -yq; \
  # Instale as dependências do pip
  pipenv install --system --deploy ; \
  # Remova o binário do wkhtmltox
  rm wkhtmltox.deb ; \
  # Remova as ferramentas necessárias para a instalação
  apt-get remove git curl -yq ; \
  # Limpeza
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
  # Instale as dependências de desenvolvimento
  pipenv install --dev --system --deploy; \
  apt-get remove git -yq; \
  apt-get autoclean -yq && apt-get autoremove -yq ; \
  rm -rf /var/lib/apt/lists/;

ENTRYPOINT []

USER 1000

CMD ["./manage.py", "runserver_plus", "0.0.0.0:8000"]