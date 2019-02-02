FROM python:3

LABEL author=felipe.lubra@gmail.com

COPY Pipfile* ./

RUN set -ex; \
pip install pipenv; \
pip install nltk;

RUN set -ex; \
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3; \
curl -f -L https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb > wkhtmltox.deb;

RUN set -ex; \
apt-get update; \
apt-get install ./wkhtmltox.deb -f --no-install-recommends -y; \
rm -rf /var/lib/apt/lists/; 

WORKDIR /app

RUN set -ex; \
pipenv install --system --deploy;

COPY . .

EXPOSE 8000

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "-w", "3", "xram_memory.wsgi" ]
