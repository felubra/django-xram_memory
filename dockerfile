FROM python:3

LABEL author=felipe.lubra@gmail.com

COPY Pipfile* package*.json ./

RUN set -ex; \
  pip install pipenv; \
  pip install nltk;

RUN set -ex; \
  curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3; \
  curl -f -L https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb > wkhtmltox.deb;

RUN set -ex; \
  apt-get update; \
  apt-get install ./wkhtmltox.deb -f --no-install-recommends -y; \
  apt-get install curl gnupg -yq; \
  curl -sL https://deb.nodesource.com/setup_8.x | bash; \
  apt-get install nodejs -yq; \
  rm -rf /var/lib/apt/lists/;

WORKDIR /app

COPY . .

RUN set -ex; \
  pipenv install --system --deploy; \
  npm ci --only=production;

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]