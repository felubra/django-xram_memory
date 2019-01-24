FROM python:3

LABEL author=felipe.lubra@gmail.com

WORKDIR /app

RUN pip install pipenv

COPY Pipfile.lock .
COPY Pipfile .

RUN pipenv install --system --deploy

RUN apt-get update && apt-get install -y --no-install-recommends \
    wkhtmltopdf \
&& rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "-w", "3", "xram_memory.wsgi" ]
