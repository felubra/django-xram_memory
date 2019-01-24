FROM python:3

LABEL author=felipe.lubra@gmail.com

RUN pip install pipenv

COPY Pipfile.lock .
COPY Pipfile .

RUN pipenv install --system --deploy

RUN set -ex; \
curl -f -L https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb > wkhtmltox.deb; \
apt-get update; \
apt-get install ./wkhtmltox.deb -f --no-install-recommends -y; \
rm -rf /var/lib/apt/lists/;

WORKDIR /app

COPY . .

EXPOSE 8000

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "-w", "3", "xram_memory.wsgi" ]
