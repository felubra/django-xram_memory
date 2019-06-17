FROM python:3

ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/share/nltk_data

LABEL author=felipe.lubra@gmail.com

WORKDIR /app

COPY scripts/download_corpora.py Pipfile* package*.json ./

RUN set -ex; \
  pip install pipenv; \
  pip install nltk; \
  python ./download_corpora.py; \
  rm ./download_corpora.py; \
  curl -f -L https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb > wkhtmltox.deb; \
  curl -sL https://deb.nodesource.com/setup_8.x | bash ;


RUN set -ex; \
  apt-get update; \
  apt-get install ./wkhtmltox.deb -f --no-install-recommends -y; \
  rm wkhtmltox.deb ; \
  apt-get install poppler-utils libmagic-dev curl gnupg python3-dev default-libmysqlclient-dev -yq; \  
  apt-get install nodejs -yq; \
  rm -rf /var/lib/apt/lists/;

RUN set -ex; \
  pipenv install --system --deploy; \
  npm ci --only=production;

COPY . .

EXPOSE 8000

USER www-data

ENTRYPOINT ["/app/entrypoint.sh"]