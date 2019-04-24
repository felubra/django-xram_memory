FROM python:3

ENV PYTHONUNBUFFERED=1

LABEL author=felipe.lubra@gmail.com

WORKDIR /app

COPY Pipfile* package*.json ./

RUN set -ex; \
  pip install pipenv; \
  pip install nltk; \
  curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3; \
  curl -f -L https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb > wkhtmltox.deb; \
  curl -sL https://deb.nodesource.com/setup_8.x | bash ;


RUN set -ex; \
  apt-get update; \
  apt-get install ./wkhtmltox.deb -f --no-install-recommends -y; \
  rm wkhtmltox.deb ; \
  apt-get install libmagic-dev curl gnupg python3-dev default-libmysqlclient-dev -yq; \
  curl -sL https://deb.nodesource.com/setup_8.x | bash ; \
  apt-get install nodejs -yq; \
  rm -rf /var/lib/apt/lists/;

RUN set -ex; \
  pipenv install --system --deploy; \
  npm ci --only=production;

COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]